import json
import subprocess
from pathlib import Path

ROOT = Path(".")
TIMELINE = ROOT / "timeline" / "reel_01.json"
OUTPUT = ROOT / "reel_01_test.mp4"
WORK = ROOT / "render_work"

WORK.mkdir(parents=True, exist_ok=True)


# =========================================================
# Utility functions
# =========================================================

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


# =========================================================
# Presenter asset resolver
# =========================================================

def find_presenter_asset(asset_path):
    """
    Finds presenter videos even if the actual filename contains
    spaces.

    Examples:
        gen1.mp4 -> gen 1.mp4
        gen2.mp4 -> gen 2.mp4
        gen3.mp4 -> gen 3.mp4
    """

    requested = ROOT / asset_path

    # 1. Exact path
    if requested.exists():
        return requested

    # 2. Alternative filenames with spaces
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

    # 3. Case-insensitive fallback
    if requested.parent.exists():
        target = filename.lower()

        for file in requested.parent.iterdir():
            if file.is_file() and file.name.lower() == target:
                return file

    return None


# =========================================================
# Placeholder renderer
# =========================================================

def render_placeholder(output, duration, shot_id):
    """
    Temporary placeholder for graphics that have not yet
    been replaced by the real motion-graphics renderer.
    """

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            (
                f"color=c=black:"
                f"s=1080x1920:"
                f"r=30:"
                f"d={duration}"
            ),
            "-vf",
            (
                "drawtext="
                "fontfile=/usr/share/fonts/truetype/dejavu/"
                "DejaVuSans-Bold.ttf:"
                f"text='SHOT {shot_id} - ASSET PENDING':"
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


# =========================================================
# Load timeline
# =========================================================

if not TIMELINE.exists():
    raise FileNotFoundError(
        f"Timeline not found: {TIMELINE}"
    )

with open(TIMELINE, "r", encoding="utf-8") as f:
    timeline = json.load(f)

shots = timeline.get("shots", [])

if not shots:
    raise RuntimeError(
        "Timeline contains no shots."
    )

print(f"Loaded {len(shots)} shots")


# =========================================================
# Render individual shots
# =========================================================

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
    # PRESENTER
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
                shot_id,
            )

        else:

            source = find_presenter_asset(asset_path)

            if source is None:

                print(
                    f"WARNING: Presenter asset not found: "
                    f"{asset_path}"
                )

                print(
                    "Available presenter assets:"
                )

                presenter_dir = ROOT / "assets" / "presenter"

                if presenter_dir.exists():

                    for file in sorted(presenter_dir.iterdir()):
                        if file.is_file():
                            print(
                                f"  - {file}"
                            )

                print(
                    "Creating temporary placeholder "
                    "so rendering can continue."
                )

                render_placeholder(
                    output,
                    duration,
                    shot_id,
                )

            else:

                print(
                    f"Using presenter asset: {source}"
                )

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
    # GRAPHIC / OTHER
    # -----------------------------------------------------

    else:

        render_placeholder(
            output,
            duration,
            shot_id,
        )

    # -----------------------------------------------------
    # Verify individual shot
    # -----------------------------------------------------

    if not output.exists():
        raise RuntimeError(
            f"Shot {shot_id} failed to render: {output}"
        )

    if output.stat().st_size == 0:
        raise RuntimeError(
            f"Shot {shot_id} is empty: {output}"
        )

    rendered_shots.append(output)

    print(
        f"SHOT {shot_id} COMPLETE: "
        f"{output} "
        f"({output.stat().st_size / 1024:.1f} KB)"
    )


# =========================================================
# Verify all rendered shots
# =========================================================

print()
print("=" * 60)
print("VERIFYING RENDERED SHOTS")
print("=" * 60)

valid_shots = []

for clip in rendered_shots:

    if clip.exists() and clip.stat().st_size > 0:

        print(
            f"OK: {clip} "
            f"({clip.stat().st_size / 1024:.1f} KB)"
        )

        valid_shots.append(clip)

    else:

        print(
            f"ERROR: Missing rendered shot: {clip}"
        )


if len(valid_shots) != len(shots):
    raise RuntimeError(
        f"Only {len(valid_shots)} of {len(shots)} shots "
        f"were rendered successfully."
    )


# =========================================================
# Create concat file
# =========================================================

concat_file = WORK / "concat.txt"

with open(concat_file, "w", encoding="utf-8") as f:

    for clip in valid_shots:

        # FFmpeg concat demuxer requires escaped single quotes
        # if paths contain them.
        clip_path = str(clip.resolve()).replace("'", "'\\''")

        f.write(
            f"file '{clip_path}'\n"
        )

print()
print(
    f"Concat file created: {concat_file}"
)


# =========================================================
# Final assembly
# =========================================================

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
        "-an",
        str(OUTPUT),
    ]
)


# =========================================================
# Final verification
# =========================================================

if not OUTPUT.exists():
    raise RuntimeError(
        "Final render was not created."
    )

if OUTPUT.stat().st_size == 0:
    raise RuntimeError(
        "Final render exists but is empty."
    )

duration = get_duration(OUTPUT)


# =========================================================
# Final report
# =========================================================

print()
print("=" * 60)
print("REEL FACTORY TEST RENDER COMPLETE")
print("=" * 60)
print(f"Output:    {OUTPUT}")
print(
    f"File size: {OUTPUT.stat().st_size / 1024:.1f} KB"
)
print(
    f"Duration:  {duration:.2f}s"
)
print(
    f"Shots:     {len(valid_shots)}/{len(shots)}"
)
print("=" * 60)
