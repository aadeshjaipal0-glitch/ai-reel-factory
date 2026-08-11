import subprocess
from pathlib import Path


# =========================================================
# GLOBAL SETTINGS
# =========================================================

ROOT = Path(".")
W = 1080
H = 1920
FPS = 30

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Style Bible palette
BLACK = "0x121212"
DARK = "0x181818"
CREAM = "0xF5F1EA"
WHITE = "0xFFFFFF"
MUTED = "0xB8B4AC"

# Single accent color
ACCENT = "0xB96B55"


# =========================================================
# FFMPEG RUNNER
# =========================================================

def run(cmd):
    print("\nRUNNING:")
    print(" ".join(str(x) for x in cmd))

    subprocess.run(cmd, check=True)


# =========================================================
# TEXT ESCAPING
# =========================================================

def escape_text(text):
    """
    Makes text safer for FFmpeg drawtext.
    """

    text = str(text)

    text = text.replace("\\", r"\\")
    text = text.replace(":", r"\:")
    text = text.replace("'", r"\'")
    text = text.replace(",", r"\,")

    return text


# =========================================================
# BASIC COLOR BACKGROUND
# =========================================================

def render_background(output, duration, color=BLACK):

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={color}:s={W}x{H}:r={FPS}:d={duration}",
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
# SIMPLE PLACEHOLDER
# =========================================================

def render_placeholder(output, duration, shot_id):

    text = escape_text(f"SHOT {shot_id}")

    vf = (
        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='{text}':"
        f"fontcolor={WHITE}:"
        f"fontsize=70:"
        f"x=(w-text_w)/2:"
        f"y=(h-text_h)/2"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={BLACK}:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            vf,
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
# HOOK CARD
# =========================================================

def render_hook(output, duration, text="AUTOMATE."):

    text = escape_text(text)

    vf = (
        f"drawbox="
        f"x=90:y=650:w=900:h=620:"
        f"color={DARK}:t=fill,"
        f"drawbox="
        f"x=90:y=650:w=12:h=620:"
        f"color={ACCENT}:t=fill,"
        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='{text}':"
        f"fontcolor={WHITE}:"
        f"fontsize=108:"
        f"x=(w-text_w)/2:"
        f"y=890"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={BLACK}:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            vf,
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
# WORKFLOW GRAPHIC
# research → script → edit → publish
# =========================================================

def render_workflow(output, duration):

    # Four nodes across the center.
    # Icons are represented with simple letters so the graphic
    # remains completely self-contained and FFmpeg-compatible.

    vf = (
        # cream card
        f"drawbox="
        f"x=70:y=570:w=940:h=760:"
        f"color={CREAM}:t=fill,"

        # accent top line
        f"drawbox="
        f"x=70:y=570:w=940:h=10:"
        f"color={ACCENT}:t=fill,"

        # connecting arrows / lines
        f"drawbox=x=270:y=940:w=170:h=8:color={ACCENT}:t=fill,"
        f"drawbox=x=510:y=940:w=170:h=8:color={ACCENT}:t=fill,"
        f"drawbox=x=750:y=940:w=170:h=8:color={ACCENT}:t=fill,"

        # node 1
        f"drawbox="
        f"x=150:y=830:w=120:h=220:"
        f"color=0xE8E0D5:t=fill,"
        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='R':"
        f"fontcolor={BLACK}:"
        f"fontsize=64:"
        f"x=183:"
        f"y=900,"

        # node 2
        f"drawbox="
        f"x=390:y=830:w=120:h=220:"
        f"color=0xE8E0D5:t=fill,"
        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='S':"
        f"fontcolor={BLACK}:"
        f"fontsize=64:"
        f"x=425:"
        f"y=900,"

        # node 3
        f"drawbox="
        f"x=630:y=830:w=120:h=220:"
        f"color=0xE8E0D5:t=fill,"
        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='E':"
        f"fontcolor={BLACK}:"
        f"fontsize=64:"
        f"x=665:"
        f"y=900,"

        # node 4
        f"drawbox="
        f"x=870:y=830:w=120:h=220:"
        f"color=0xE8E0D5:t=fill,"
        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='P':"
        f"fontcolor={BLACK}:"
        f"fontsize=64:"
        f"x=905:"
        f"y=900,"

        # title
        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='CONTENT WORKFLOW':"
        f"fontcolor={BLACK}:"
        f"fontsize=58:"
        f"x=(w-text_w)/2:"
        f"y=680"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={BLACK}:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            vf,
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
# AGENT PIPELINE
# =========================================================

def render_agent_pipeline(output, duration):

    vf = (
        f"drawbox="
        f"x=80:y=500:w=920:h=900:"
        f"color={CREAM}:t=fill,"

        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='AI AGENT':"
        f"fontcolor={BLACK}:"
        f"fontsize=70:"
        f"x=(w-text_w)/2:"
        f"y=600,"

        # central agent
        f"drawbox="
        f"x=390:y=790:w=300:h=220:"
        f"color={ACCENT}:t=fill,"
        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='AGENT':"
        f"fontcolor={WHITE}:"
        f"fontsize=62:"
        f"x=(w-text_w)/2:"
        f"y=865,"

        # input/output blocks
        f"drawbox=x=130:y=830:w=180:h=140:color=0xE8E0D5:t=fill,"
        f"drawbox=x=770:y=830:w=180:h=140:color=0xE8E0D5:t=fill,"

        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='INPUT':"
        f"fontcolor={BLACK}:"
        f"fontsize=38:"
        f"x=173:"
        f"y=880,"

        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='OUTPUT':"
        f"fontcolor={BLACK}:"
        f"fontsize=38:"
        f"x=795:"
        f"y=880,"

        # connections
        f"drawbox=x=310:y=895:w=80:h=8:color={ACCENT}:t=fill,"
        f"drawbox=x=690:y=895:w=80:h=8:color={ACCENT}:t=fill"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={BLACK}:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            vf,
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
# TIMELINE GRAPHIC
# =========================================================

def render_timeline(output, duration):

    vf = (
        f"drawbox="
        f"x=70:y=600:w=940:h=700:"
        f"color={CREAM}:t=fill,"

        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='AUTOMATED TIMELINE':"
        f"fontcolor={BLACK}:"
        f"fontsize=62:"
        f"x=(w-text_w)/2:"
        f"y=700,"

        # timeline rail
        f"drawbox="
        f"x=140:y=980:w=800:h=10:"
        f"color={MUTED}:t=fill,"

        # clips
        f"drawbox=x=150:y=900:w=150:h=150:color={ACCENT}:t=fill,"
        f"drawbox=x=330:y=900:w=180:h=150:color=0xD7D0C5:t=fill,"
        f"drawbox=x=540:y=900:w=150:h=150:color={ACCENT}:t=fill,"
        f"drawbox=x=720:y=900:w=200:h=150:color=0xD7D0C5:t=fill,"

        # playhead
        f"drawbox="
        f"x=600:y=850:w=6:h=240:"
        f"color={BLACK}:t=fill"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={BLACK}:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            vf,
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
# DASHBOARD / ANALYTICS
# =========================================================

def render_dashboard(output, duration):

    vf = (
        f"drawbox="
        f"x=70:y=560:w=940:h=800:"
        f"color={CREAM}:t=fill,"

        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='AUTOMATION':"
        f"fontcolor={BLACK}:"
        f"fontsize=64:"
        f"x=140:"
        f"y=660,"

        # bars
        f"drawbox=x=180:y=1120:w=110:h=120:color={MUTED}:t=fill,"
        f"drawbox=x=340:y=1020:w=110:h=220:color={ACCENT}:t=fill,"
        f"drawbox=x=500:y=900:w=110:h=340:color={MUTED}:t=fill,"
        f"drawbox=x=660:y=780:w=110:h=460:color={ACCENT}:t=fill,"
        f"drawbox=x=820:y=680:w=110:h=560:color={MUTED}:t=fill,"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={BLACK}:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            vf,
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
# TEXT CARD
# =========================================================

def render_text_card(
    output,
    duration,
    text,
    background=BLACK,
    font_size=90,
):

    if background == "cream":
        bg = CREAM
        fg = BLACK
    else:
        bg = BLACK
        fg = WHITE

    text = escape_text(text)

    vf = (
        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='{text}':"
        f"fontcolor={fg}:"
        f"fontsize={font_size}:"
        f"x=(w-text_w)/2:"
        f"y=(h-text_h)/2"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={bg}:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            vf,
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
# CHAPTER MARKER
# =========================================================

def render_chapter(output, duration, title):

    title = escape_text(title)

    vf = (
        f"drawbox="
        f"x=90:y=720:w=900:h=480:"
        f"color={CREAM}:t=fill,"

        f"drawbox="
        f"x=90:y=720:w=16:h=480:"
        f"color={ACCENT}:t=fill,"

        f"drawtext="
        f"fontfile={FONT_BOLD}:"
        f"text='{title}':"
        f"fontcolor={BLACK}:"
        f"fontsize=76:"
        f"x=150:"
        f"y=900"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={BLACK}:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            vf,
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
# GRAPHIC DISPATCHER
# =========================================================

def render_graphic(output, shot):

    duration = float(shot["duration"])

    graphic = str(
        shot.get("graphic", "placeholder")
    ).lower()

    if graphic == "hook":
        render_hook(
            output,
            duration,
            shot.get("text", "AUTOMATE.")
        )

    elif graphic == "workflow":
        render_workflow(
            output,
            duration
        )

    elif graphic in (
        "agent",
        "agent_pipeline",
        "pipeline",
    ):
        render_agent_pipeline(
            output,
            duration
        )

    elif graphic == "timeline":
        render_timeline(
            output,
            duration
        )

    elif graphic in (
        "dashboard",
        "analytics",
    ):
        render_dashboard(
            output,
            duration
        )

    elif graphic == "chapter":
        render_chapter(
            output,
            duration,
            shot.get("title", "AUTOMATION")
        )

    elif graphic == "text":
        render_text_card(
            output,
            duration,
            shot.get("text", "TEXT"),
            shot.get("background", BLACK),
            int(shot.get("font_size", 90)),
        )

    else:
        render_placeholder(
            output,
            duration,
            shot.get("id", "?")
        )


# =========================================================
# PUBLIC FUNCTION USED BY render.py
# =========================================================

def render_graphic_shot(output, shot):
    """
    Main public function.

    render.py should call:

        render_graphic_shot(output, shot)

    This keeps graphics.py reusable for every future reel.
    """

    render_graphic(
        output,
        shot
    )
