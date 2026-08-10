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
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file)
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return float(result.stdout.strip())


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
    duration = shot["duration"]
    shot_type = shot["type"]

    output = WORK / f"shot_{shot_id:02d}.mp4"

    print(
        f"Rendering Shot {shot_id} | "
        f"type={shot_type} | "
        f"duration={duration}s"
    )

    if shot_type == "presenter":

        source = ROOT / shot["asset"]

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

            "-an",

            str(output)
        ])

    else:

        # Temporary placeholder for non-presenter shots.
        # These will later be replaced by the real
        # graphics / motion-graphics renderer.

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

            "-an",

            str(output)
        ])

    rendered_shots.append(output)


# ---------------------------------------------------------
# Create concat file
# ---------------------------------------------------------

concat_file = WORK / "concat.txt"

with open(concat_file, "w", encoding="utf-8") as f:

    for clip in rendered_shots:
        f.write(f"file '{clip.resolve()}'\n")


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

    str(OUTPUT)
])


duration = get_duration(OUTPUT)

print()
print("========================================")
print("REEL FACTORY TEST RENDER COMPLETE")
print("========================================")
print(f"Output: {OUTPUT}")
print(f"Duration: {duration:.2f}s")
print("========================================")
