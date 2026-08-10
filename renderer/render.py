import json
import subprocess
from pathlib import Path

ROOT = Path(".")
TIMELINE = ROOT / "timeline" / "reel_01.json"
OUTPUT = ROOT / "reel_01_test.mp4"
WORK = ROOT / "render_work"

WORK.mkdir(exist_ok=True)


def run(cmd):
    print("RUNNING:", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def get_duration(file):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return float(result.stdout.strip())


def find_presenter_asset(asset_path):
    """
    Resolves presenter files even if filenames contain spaces.

    Example:
    gen1.mp4  -> gen 1.mp4
    gen2.mp4  -> gen 2.mp4
    gen3.mp4  -> gen 3.mp4
    """

    requested = ROOT / asset_path

    # Exact path exists
    if requested.exists():
        return requested

    # Try replacing gen1/gen2/gen3 with gen 1/gen 2/gen 3
    filename = requested.name

    replacements = {
        "gen1.mp4": "gen 1.mp4",
        "gen2.mp4": "gen 2.mp4",
        "gen3.mp4": "gen 3.mp4",
        "gen4.mp4": "gen 4.mp4",
    }

    if filename in replacements:
        alternative = requested.parent / replacements[filename]

        if alternative.exists():
            return alternative

    return None


def render_placeholder(output, duration, shot_id):
    """
    Temporary placeholder for shots whose real visual asset
    has not been generated yet.
    """

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c=black:s=1080x1920:r=30:d={duration}",
            "-vf",
            (
                "drawtext="
                "fontfile=/usr/share/fonts/truetype/dejavu/"
                "DejaVuSans-Bold.ttf:"
                f"text='SHOT {shot_id} — ASSET PENDING':"
                "fontcolor=white:"
                "fontsize=70:"
                "x=(w-text_w)/2:"
                "y=(h-text_h)/2"
            ),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(output),
        ]
    )


# ---------------------------------------------------------
# Load timeline
# ---------------------------------------------------------

if not TIMELINE.exists():
    raise FileNotFoundError(
        f"Timeline not found: {TIMELINE}"
    )


with open(TIMELINE, "r", encoding="utf-8") as f:
    timeline = json.load(f)


shots = timeline["shots"]

print(f"Loaded {len(shots)} shots")


# ---------------------------------------------------------
# Render individual shots
# ---------------------------------------------------------

rendered_shots = []


for shot in shots:

    shot_id = int(shot["id"])
    duration = float(shot["duration"])
    shot_type = shot["type"]

    output = WORK / f"shot_{shot_id:02d}.mp4"

    print()
    print("=" * 60)
    print(
        f"Rendering Shot {shot_id} | "
        f"type={shot_type} | "
        f"duration={duration}s"
    )
    print("=" * 60)

    # -----------------------------------------------------
    # PRESENTER SHOT
    # -----------------------------------------------------

    if shot_type == "presenter":

        asset_path = shot.get("asset")

        if not asset_path:
            print(
                f"WARNING: Shot {shot_id} has no presenter asset."
            )

            render_placeholder(
                output,
                duration,
                shot_id
            )

        else:

            source = find_presenter_asset(asset_path)

            if source is None:

                print(
                    f"WARNING: Presenter asset not found: "
                    f"{asset_path}"
                )

                print(
                    "Creating temporary placeholder so "
                    "the test render can continue."
                )

                render_placeholder(
                    output,
                    duration,
                    shot_id
                )

            else:

                print(f"Using presenter asset: {source}")

                run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        str(source),
                        "-t",
                        str(duration),
                        "-vf",
                        (
                            "scale=1080:1920:"
                            "force_original_aspect_ratio=increase,"
                            "crop=1080:1920,"
                            "setsar=1"
                        ),
                        "-r",
                        "30",
                        "-c:v",
                        "libx264",
                        "-preset",
                        "veryfast",
                        "-pix_fmt",
                        "yuv420p",
                        "-an",
                        str(output),
                    ]
                )

    # -----------------------------------------------------
    # NON-PRESENTER SHOT
    # -----------------------------------------------------

    else:

        render_placeholder(
            output,
            duration,
            shot_id
        )

    rendered_shots.append(output)


# ---------------------------------------------------------
# Verify rendered shots
# ---------------------------------------------------------

print()
print("=" * 60)
print("VERIFYING SHOTS")
print("=" * 60)

valid_shots = []

for clip in rendered_shots:

    if clip.exists() and clip.stat().st_size > 0:

        print(
            f"OK: {clip} "
            f"({clip.stat().st_size} bytes)"
        )

        valid_shots.append(clip)

    else:

        print(
            f"ERROR: Missing rendered shot: {clip}"
        )


if not valid_shots:
    raise RuntimeError(
        "No valid shots were rendered."
    )


# ---------------------------------------------------------
# Create concat file
# ---------------------------------------------------------

concat_file = WORK / "concat.txt"

with open(concat_file, "w", encoding="utf-8") as f:

    for clip in valid_shots:
        f.write(
            f"file '{clip.resolve()}'\n"
        )


print()
print(f"Concat file created: {concat_file}")


# ---------------------------------------------------------
# Final assembly
# ---------------------------------------------------------

run(
    [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        str(OUTPUT),
    ]
)


# ---------------------------------------------------------
# Final verification
# ---------------------------------------------------------

if not OUTPUT.exists():
    raise RuntimeError(
        "Final render was not created."
    )


duration = get_duration(OUTPUT)


print()
print("=" * 60)
print("REEL FACTORY TEST RENDER COMPLETE")
print("=" * 60)
print(f"Output: {OUTPUT}")
print(f"File size: {OUTPUT.stat().st_size / 1024:.1f} KB")
print(f"Duration: {duration:.2f}s")
print("=" * 60)
