from pathlib import Path
import subprocess


WIDTH = 1080
HEIGHT = 1920
FPS = 30

ROOT = Path(".")
WORK = ROOT / "render_work"


def run(cmd):
    print("GRAPHICS:", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def render_graphic(shot, output):
    """
    Reusable graphic renderer.

    Supported templates:
    - icon
    - typography
    - dashboard
    - split_workflow
    - split_timeline
    """

    duration = float(shot["duration"])
    template = shot.get("template", "placeholder")

    if template == "icon":
        render_icon(
            output,
            duration,
            shot.get("icon", "spark"),
        )

    elif template == "typography":
        render_typography(
            output,
            duration,
            shot.get("text", ""),
        )

    elif template == "dashboard":
        render_dashboard(output, duration)

    elif template == "split_workflow":
        render_split_graphic(
            output,
            duration,
            "WORKFLOW",
        )

    elif template == "split_timeline":
        render_split_graphic(
            output,
            duration,
            "TIMELINE",
        )

    else:
        render_placeholder(
            output,
            duration,
            shot["id"],
        )


# ---------------------------------------------------------
# ICON
# ---------------------------------------------------------

def render_icon(output, duration, icon_name):

    # Temporary procedural icon system.
    # We will replace these text symbols with SVG icons
    # after the template pipeline is verified.

    symbols = {
        "gear_spark": "⚙",
        "magnifier": "⌕",
        "pencil": "✎",
        "clapperboard": "▣",
        "rocket": "▲",
        "spark": "✦",
    }

    symbol = symbols.get(icon_name, "✦")

    filter_text = (
        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/"
        "DejaVuSans.ttf:"
        f"text='{symbol}':"
        "fontcolor=white:"
        "fontsize=180:"
        "x=(w-text_w)/2:"
        "y=(h-text_h)/2"
    )

    run([
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x111111:s={WIDTH}x{HEIGHT}:r={FPS}:d={duration}",
        "-vf",
        filter_text,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-an",
        str(output),
    ])


# ---------------------------------------------------------
# TYPOGRAPHY
# ---------------------------------------------------------

def render_typography(output, duration, text):

    filter_text = (
        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/"
        "DejaVuSans-Bold.ttf:"
        f"text='{text}':"
        "fontcolor=white:"
        "fontsize=110:"
        "x=(w-text_w)/2:"
        "y=(h-text_h)/2:"
        "enable='between(t,0,"
        f"{duration})'"
    )

    run([
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x111111:s={WIDTH}x{HEIGHT}:r={FPS}:d={duration}",
        "-vf",
        filter_text,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-an",
        str(output),
    ])


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

def render_dashboard(output, duration):

    filter_text = (
        "drawbox="
        "x=100:y=350:w=880:h=900:"
        "color=0x222222@1:"
        "t=fill,"
        "drawbox="
        "x=160:y=450:w=760:h=120:"
        "color=0x444444@1:"
        "t=fill,"
        "drawbox="
        "x=160:y=650:w=500:h=25:"
        "color=white@0.8:"
        "t=fill,"
        "drawbox="
        "x=160:y=720:w=650:h=25:"
        "color=white@0.5:"
        "t=fill"
    )

    run([
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x111111:s={WIDTH}x{HEIGHT}:r={FPS}:d={duration}",
        "-vf",
        filter_text,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-an",
        str(output),
    ])


# ---------------------------------------------------------
# SPLIT GRAPHICS
# ---------------------------------------------------------

def render_split_graphic(output, duration, label):

    filter_text = (
        "drawbox="
        "x=70:y=100:w=940:h=600:"
        "color=0x1d1d1d@1:"
        "t=fill,"
        "drawbox="
        "x=140:y=250:w=180:h=100:"
        "color=0x333333@1:"
        "t=fill,"
        "drawbox="
        "x=450:y=250:w=180:h=100:"
        "color=0x333333@1:"
        "t=fill,"
        "drawbox="
        "x=760:y=250:w=180:h=100:"
        "color=0x333333@1:"
        "t=fill,"
        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/"
        "DejaVuSans-Bold.ttf:"
        f"text='{label}':"
        "fontcolor=white:"
        "fontsize=70:"
        "x=(w-text_w)/2:"
        "y=480"
    )

    run([
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=black:s={WIDTH}x{HEIGHT}:r={FPS}:d={duration}",
        "-vf",
        filter_text,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-an",
        str(output),
    ])


# ---------------------------------------------------------
# FALLBACK
# ---------------------------------------------------------

def render_placeholder(output, duration, shot_id):

    filter_text = (
        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/"
        "DejaVuSans-Bold.ttf:"
        f"text='SHOT {shot_id}':"
        "fontcolor=white:"
        "fontsize=80:"
        "x=(w-text_w)/2:"
        "y=(h-text_h)/2"
    )

    run([
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=black:s={WIDTH}x{HEIGHT}:r={FPS}:d={duration}",
        "-vf",
        filter_text,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-an",
        str(output),
    ])
