import json
import subprocess
from pathlib import Path

ROOT = Path(".")
TIMELINE = ROOT / "timeline" / "reel_01.json"
OUTPUT = ROOT / "reel_01_test.mp4"
WORK = ROOT / "render_work"

W = 1080
H = 1920
FPS = 30

WORK.mkdir(exist_ok=True)


# =========================================================
# COMMAND RUNNER
# =========================================================

def run(cmd):
    print("\nRUNNING:")
    print(" ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


# =========================================================
# DURATION
# =========================================================

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


# =========================================================
# PRESENTER ASSET FINDER
# =========================================================

def find_presenter_asset(asset_path):
    requested = ROOT / asset_path

    if requested.exists():
        return requested

    filename = requested.name

    alternatives = {
        "gen1.mp4": "gen 1.mp4",
        "gen2.mp4": "gen 2.mp4",
        "gen3.mp4": "gen 3.mp4",
        "gen4.mp4": "gen 4.mp4",
    }

    if filename in alternatives:
        alternative = requested.parent / alternatives[filename]

        if alternative.exists():
            return alternative

    return None


# =========================================================
# GENERIC BLACK / PLACEHOLDER
# =========================================================

def render_placeholder(output, duration, text):
    run(
        [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i",
            f"color=c=black:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            (
                "drawtext="
                "fontfile=/usr/share/fonts/truetype/dejavu/"
                "DejaVuSans-Bold.ttf:"
                f"text='{text}':"
                "fontcolor=white:"
                "fontsize=70:"
                "x=(w-text_w)/2:"
                "y=(h-text_h)/2"
            ),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output),
        ]
    )


# =========================================================
# RADIAL BACKGROUND
# =========================================================

def render_radial_background(output, duration):
    run(
        [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i",
            f"color=c=0x111111:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            (
                "vignette="
                "angle=PI/5:"
                "mode=forward"
            ),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output),
        ]
    )


# =========================================================
# TEXT CARD
# =========================================================

def render_text_card(output, duration, text, background="black"):
    font = (
        "/usr/share/fonts/truetype/dejavu/"
        "DejaVuSans-Bold.ttf"
    )

    if background == "cream":
        bg = "0xF4EFE6"
        fg = "0x111111"
    else:
        bg = "0x080808"
        fg = "white"

    safe_text = text.replace("'", r"\'")

    run(
        [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i",
            f"color=c={bg}:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            (
                "drawtext="
                f"fontfile={font}:"
                f"text='{safe_text}':"
                f"fontcolor={fg}:"
                "fontsize=90:"
                "x=(w-text_w)/2:"
                "y=(h-text_h)/2:"
                "box=0"
            ),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output),
        ]
    )


# =========================================================
# ICON CARD
# =========================================================

def render_icon_card(output, duration, icon_name):
    font = (
        "/usr/share/fonts/truetype/dejavu/"
        "DejaVuSans-Bold.ttf"
    )

    safe_icon = icon_name.replace("'", r"\'")

    run(
        [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i",
            f"color=c=0x101010:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            (
                "drawbox="
                "x=190:y=600:w=700:h=700:"
                "color=0x1C1C1C:"
                "t=fill,"
                "drawtext="
                f"fontfile={font}:"
                f"text='{safe_icon}':"
                "fontcolor=white:"
                "fontsize=120:"
                "x=(w-text_w)/2:"
                "y=(h-text_h)/2"
            ),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output),
        ]
    )


# =========================================================
# PRESENTER
# =========================================================

def render_presenter(output, source, duration):
    run(
        [
            "ffmpeg",
            "-y",
            "-i", str(source),

            "-t", str(duration),

            "-vf",
            (
                "scale="
                f"{W}:{H}:"
                "force_original_aspect_ratio=increase,"
                f"crop={W}:{H},"
                "setsar=1"
            ),

            "-r", str(FPS),

            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",

            # KEEP ORIGINAL AUDIO
            "-c:a", "aac",
            "-b:a", "192k",

            str(output),
        ]
    )


# =========================================================
# GRAPHIC DISPATCHER
# =========================================================

def render_graphic(output, shot):
    duration = float(shot["duration"])

    graphic = shot.get("graphic", "placeholder")

    if graphic == "radial":
        render_radial_background(
            output,
            duration
        )

    elif graphic == "text":
        render_text_card(
            output,
            duration,
            shot.get("text", "TEXT"),
            shot.get("background", "black")
        )

    elif graphic == "icon":
        render_icon_card(
            output,
            duration,
            shot.get("icon", "AI")
        )

    elif graphic == "workflow":
        render_icon_card(
            output,
            duration,
            "WORKFLOW"
        )

    elif graphic == "dashboard":
        render_icon_card(
            output,
            duration,
            "ANALYTICS"
        )

    elif graphic == "timeline":
        render_icon_card(
            output,
            duration,
            "TIMELINE"
        )

    else:
        render_placeholder(
            output,
            duration,
            f"SHOT {shot['id']}"
        )


# =========================================================
# LOAD TIMELINE
# =========================================================

if not TIMELINE.exists():
    raise FileNotFoundError(
        f"Timeline not found: {TIMELINE}"
    )

with open(TIMELINE, "r", encoding="utf-8") as f:
    timeline = json.load(f)

shots = timeline["shots"]

print(f"\nLoaded {len(shots)} shots")


# =========================================================
# RENDER SHOTS
# =========================================================

rendered_shots = []

for shot in shots:

    shot_id = int(shot["id"])
    duration = float(shot["duration"])
    shot_type = shot["type"]

    output = WORK / f"shot_{shot_id:02d}.mp4"

    print("\n" + "=" * 70)
    print(
        f"SHOT {shot_id} | "
        f"TYPE={shot_type} | "
        f"DURATION={duration}s"
    )
    print("=" * 70)

    # -----------------------------------------------------
    # PRESENTER
    # -----------------------------------------------------

    if shot_type == "presenter":

        asset_path = shot.get("asset")

        if not asset_path:
            print("WARNING: No presenter asset specified.")

            render_placeholder(
                output,
                duration,
                f"SHOT {shot_id} — PRESENTER MISSING"
            )

        else:

            source = find_presenter_asset(asset_path)

            if source is None:

                print(
                    f"WARNING: Presenter asset not found: "
                    f"{asset_path}"
                )

                render_placeholder(
                    output,
                    duration,
                    f"SHOT {shot_id} — ASSET MISSING"
                )

            else:

                print(f"Presenter: {source}")

                render_presenter(
                    output,
                    source,
                    duration
                )

    # -----------------------------------------------------
    # GRAPHICS
    # -----------------------------------------------------

    else:

        render_graphic(
            output,
            shot
        )

    rendered_shots.append(output)


# =========================================================
# VERIFY SHOTS
# =========================================================

print("\n" + "=" * 70)
print("VERIFYING RENDERED SHOTS")
print("=" * 70)

valid_shots = []

for clip in rendered_shots:

    if clip.exists() and clip.stat().st_size > 0:

        print(
            f"OK  {clip} "
            f"({clip.stat().st_size / 1024:.1f} KB)"
        )

        valid_shots.append(clip)

    else:

        print(
            f"ERROR: Missing {clip}"
        )


if not valid_shots:
    raise RuntimeError(
        "No valid rendered shots."
    )


# =========================================================
# CONCAT FILE
# =========================================================

concat_file = WORK / "concat.txt"

with open(
    concat_file,
    "w",
    encoding="utf-8"
) as f:

    for clip in valid_shots:

        f.write(
            f"file '{clip.resolve()}'\n"
        )

print(
    f"\nConcat file created: "
    f"{concat_file}"
)


# =========================================================
# FINAL ASSEMBLY
# =========================================================

print("\n" + "=" * 70)
print("ASSEMBLING FINAL REEL")
print("=" * 70)

run(
    [
        "ffmpeg",
        "-y",

        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),

        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",

        # AAC output
        "-c:a", "aac",
        "-b:a", "192k",

        str(OUTPUT),
    ]
)


# =========================================================
# FINAL VERIFICATION
# =========================================================

if not OUTPUT.exists():
    raise RuntimeError(
        "Final reel was not created."
    )

duration = get_duration(OUTPUT)

print("\n")
print("=" * 70)
print("REEL FACTORY TEST RENDER COMPLETE")
print("=" * 70)
print(f"OUTPUT: {OUTPUT}")
print(
    f"SIZE: "
    f"{OUTPUT.stat().st_size / 1024:.1f} KB"
)
print(f"DURATION: {duration:.2f}s")
print("=" * 70)
