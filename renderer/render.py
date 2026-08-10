import json
import subprocess
from pathlib import Path

ROOT = Path(".")
TIMELINE = ROOT / "timeline" / "reel_01.json"
OUTPUT = ROOT / "final_reel.mp4"
WORK = ROOT / "render_work"

WORK.mkdir(exist_ok=True)


def run(cmd):
    print("RUNNING:", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def get_duration(file):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return float(result.stdout.strip())


def resolve_asset(asset_path):
    """
    Resolve presenter asset paths.
    Supports both:
      gen1.mp4
      gen 1.mp4
    """

    source = ROOT / asset_path

    if source.exists():
        return source

    # Fix gen1 -> gen 1 automatically
    filename = source.name.lower()

    replacements = {
        "gen1.mp4": "gen 1.mp4",
        "gen2.mp4": "gen 2.mp4",
        "gen3.mp4": "gen 3.mp4",
    }

    if filename in replacements:
        alternative = source.parent / replacements[filename]

        if alternative.exists():
            print(f"Asset path corrected: {source} -> {alternative}")
            return alternative

    raise FileNotFoundError(
        f"\nAsset not found:\n"
        f"Requested: {source}\n"
        f"Please check the filename in assets/presenter/\n"
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
# Create individual shot clips
# ---------------------------------------------------------

rendered_shots = []

for shot in shots:

    shot_id = shot["id"]
    duration = float(shot["duration"])
    shot_type = shot["type"]

    output = WORK / f"shot_{shot_id:02d}.mp4"

    print(
        f"\nRendering Shot {shot_id} | "
        f"type={shot_type} | "
        f"duration={duration}s"
    )

    # -----------------------------------------------------
    # PRESENTER SHOT
    # -----------------------------------------------------

    if shot_type == "presenter":

        source = resolve_asset(shot["asset"])

        run([
            "ffmpeg",
            "-y",

            "-i", str(source),

            "-t", str(duration),

            "-vf",
            (
                "scale=1080:1920:"
                "force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "setsar=1"
            ),

            "-r", "30",

            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",

            # Keep presenter audio
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "48000",

            "-shortest",

            str(output),
        ])

    # -----------------------------------------------------
    # NON-PRESENTER SHOT
    # -----------------------------------------------------

    else:

        # Temporary graphic placeholder.
        # Later this will be replaced with the real
        # motion graphics / SVG / UI renderer.

        run([
            "ffmpeg",
            "-y",

            "-f", "lavfi",
            "-i",
            (
                f"color=c=black:"
                f"s=1080x1920:"
                f"r=30:"
                f"d={duration}"
            ),

            # Generate silent audio so every clip has
            # compatible audio/video streams for concat.
            "-f", "lavfi",
            "-i",
            (
                "anullsrc="
                "channel_layout=stereo:"
                "sample_rate=48000"
            ),

            "-t", str(duration),

            "-vf",
            (
                "drawtext="
                "fontfile=/usr/share/fonts/truetype/dejavu/"
                "DejaVuSans-Bold.ttf:"
                f"text='SHOT {shot_id}':"
                "fontcolor=white:"
                "fontsize=80:"
                "x=(w-text_w)/2:"
                "y=(h-text_h)/2"
            ),

            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",

            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "48000",
            "-ac", "2",

            "-shortest",

            str(output),
        ])

    rendered_shots.append(output)


# ---------------------------------------------------------
# Create concat file
# ---------------------------------------------------------

concat_file = WORK / "concat.txt"

with open(concat_file, "w", encoding="utf-8") as f:

    for clip in rendered_shots:
        f.write(f"file '{clip.resolve()}'\n")


print(f"\nConcat file created: {concat_file}")
print(f"Shots ready for assembly: {len(rendered_shots)}")


# ---------------------------------------------------------
# Final assembly
# ---------------------------------------------------------

run([
    "ffmpeg",
    "-y",

    "-f", "concat",
    "-safe", "0",

    "-i", str(concat_file),

    "-c:v", "libx264",
    "-preset", "veryfast",
    "-pix_fmt", "yuv420p",

    "-c:a", "aac",
    "-b:a", "128k",
    "-ar", "48000",
    "-ac", "2",

    str(OUTPUT),
])


# ---------------------------------------------------------
# Verify final output
# ---------------------------------------------------------

duration = get_duration(OUTPUT)

print()
print("========================================")
print("REEL FACTORY TEST RENDER COMPLETE")
print("========================================")
print(f"Output: {OUTPUT}")
print(f"Duration: {duration:.2f}s")
print(f"Shots: {len(rendered_shots)}")
print("========================================")
