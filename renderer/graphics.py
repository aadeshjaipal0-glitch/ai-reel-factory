import subprocess
from pathlib import Path

W = 1080
H = 1920
FPS = 30

FONT_BOLD = (
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans-Bold.ttf"
)

FONT_REGULAR = (
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans.ttf"
)


def run(cmd):
    print("GRAPHIC:", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def render_graphic(output, shot):
    graphic = shot.get("graphic", "hook")
    duration = float(shot["duration"])

    if graphic == "hook":
        return hook(output, duration, shot)

    if graphic == "workflow":
        return workflow(output, duration, shot)

    if graphic == "search":
        return search(output, duration)

    if graphic == "dashboard":
        return dashboard(output, duration)

    if graphic == "automation":
        return automation(output, duration)

    if graphic == "script":
        return script_card(output, duration)

    if graphic == "generate":
        return generate(output, duration)

    if graphic == "timeline":
        return timeline(output, duration)

    if graphic == "publish":
        return publish(output, duration)

    if graphic == "zero_editing":
        return zero_editing(output, duration, shot)

    return hook(output, duration, shot)


# =========================================================
# HOOK
# =========================================================

def hook(output, duration, shot):
    title = shot.get("title", "AI IS CHANGING")
    subtitle = shot.get("subtitle", "EVERYTHING")

    vf = (
        f"drawbox=x=80:y=560:w=920:h=800:"
        f"color=0x171717@1:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        f"text='{title}':"
        f"fontcolor=white:"
        f"fontsize=88:"
        f"x=(w-text_w)/2:"
        f"y=760,"
        f"drawtext=fontfile={FONT_BOLD}:"
        f"text='{subtitle}':"
        f"fontcolor=white:"
        f"fontsize=112:"
        f"x=(w-text_w)/2:"
        f"y=900"
    )

    render_base(output, duration, vf)


# =========================================================
# WORKFLOW
# =========================================================

def workflow(output, duration, shot):
    nodes = shot.get(
        "nodes",
        ["RESEARCH", "SCRIPT", "CREATE", "PUBLISH"]
    )

    filters = []

    y = 500

    for i, node in enumerate(nodes):

        x = 90 + i * 245

        filters.append(
            f"drawbox="
            f"x={x}:y={y}:"
            f"w=205:h=180:"
            f"color=0x202020@1:"
            f"t=fill"
        )

        filters.append(
            f"drawtext="
            f"fontfile={FONT_BOLD}:"
            f"text='{node}':"
            f"fontcolor=white:"
            f"fontsize=30:"
            f"x={x}+102-text_w/2:"
            f"y={y}+78"
        )

        if i < len(nodes) - 1:
            filters.append(
                f"drawtext="
                f"fontfile={FONT_BOLD}:"
                f"text='→':"
                f"fontcolor=white:"
                f"fontsize=50:"
                f"x={x+210}:"
                f"y={y+62}"
            )

    render_base(
        output,
        duration,
        ",".join(filters)
    )


# =========================================================
# SEARCH
# =========================================================

def search(output, duration):
    vf = (
        "drawbox=x=100:y=650:w=880:h=170:"
        "color=0x202020:t=fill,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='Search anything...':"
        "fontcolor=0xAAAAAA:"
        "fontsize=48:"
        "x=155:y=710,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='⌕':"
        "fontcolor=white:"
        "fontsize=65:"
        "x=900:y=695"
    )

    render_base(output, duration, vf)


# =========================================================
# DASHBOARD
# =========================================================

def dashboard(output, duration):
    vf = (
        "drawbox=x=100:y=430:w=880:h=900:"
        "color=0x171717:t=fill,"
        "drawtext="
        f"fontfile={FONT_BOLD}:"
        "text='AI DASHBOARD':"
        "fontcolor=white:"
        "fontsize=55:"
        "x=150:y=500,"
        "drawbox=x=160:y=650:w=220:h=450:"
        "color=0x303030:t=fill,"
        "drawbox=x=430:y=750:w=220:h=350:"
        "color=0x303030:t=fill,"
        "drawbox=x=700:y=590:w=180:h=510:"
        "color=0x303030:t=fill"
    )

    render_base(output, duration, vf)


# =========================================================
# AUTOMATION
# =========================================================

def automation(output, duration):
    vf = (
        "drawbox=x=150:y=650:w=780:h=180:"
        "color=0x202020:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='AUTOMATION':"
        "fontcolor=white:"
        "fontsize=65:"
        "x=(w-text_w)/2:"
        "y=710,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='ONE INPUT → MANY OUTPUTS':"
        "fontcolor=0xAAAAAA:"
        "fontsize=35:"
        "x=(w-text_w)/2:"
        "y=860"
    )

    render_base(output, duration, vf)


# =========================================================
# SCRIPT
# =========================================================

def script_card(output, duration):
    vf = (
        "drawbox=x=130:y=480:w=820:h=1000:"
        "color=0x171717:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='SCRIPT':"
        "fontcolor=white:"
        "fontsize=65:"
        "x=190:y=560,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='Write → Refine → Approve':"
        "fontcolor=0xAAAAAA:"
        "fontsize=42:"
        "x=190:y=680"
    )

    render_base(output, duration, vf)


# =========================================================
# GENERATE
# =========================================================

def generate(output, duration):
    vf = (
        "drawbox=x=150:y=620:w=780:h=300:"
        "color=0x202020:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='GENERATE':"
        "fontcolor=white:"
        "fontsize=75:"
        "x=(w-text_w)/2:"
        "y=720"
    )

    render_base(output, duration, vf)


# =========================================================
# TIMELINE
# =========================================================

def timeline(output, duration):
    vf = (
        "drawbox=x=100:y=700:w=880:h=20:"
        "color=0x404040:t=fill,"
        "drawbox=x=100:y=700:w=600:h=20:"
        "color=white:t=fill,"
        "drawbox=x=170:y=580:w=150:h=70:"
        "color=0x202020:t=fill,"
        "drawbox=x=360:y=580:w=210:h=70:"
        "color=0x202020:t=fill,"
        "drawbox=x=610:y=580:w=180:h=70:"
        "color=0x202020:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='TIMELINE':"
        "fontcolor=white:"
        "fontsize=65:"
        "x=(w-text_w)/2:"
        "y=450"
    )

    render_base(output, duration, vf)


# =========================================================
# PUBLISH
# =========================================================

def publish(output, duration):
    vf = (
        "drawbox=x=180:y=650:w=720:h=250:"
        "color=0x202020:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='PUBLISH':"
        "fontcolor=white:"
        "fontsize=80:"
        "x=(w-text_w)/2:"
        "y=735"
    )

    render_base(output, duration, vf)


# =========================================================
# ZERO EDITING
# =========================================================

def zero_editing(output, duration, shot):
    title = shot.get("title", "ZERO EDITING")
    subtitle = shot.get(
        "subtitle",
        "AUTOMATED WORKFLOW"
    )

    vf = (
        f"drawtext=fontfile={FONT_BOLD}:"
        f"text='{title}':"
        "fontcolor=white:"
        "fontsize=105:"
        "x=(w-text_w)/2:"
        "y=720,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        f"text='{subtitle}':"
        "fontcolor=0xAAAAAA:"
        "fontsize=42:"
        "x=(w-text_w)/2:"
        "y=860"
    )

    render_base(output, duration, vf)


# =========================================================
# BASE RENDER
# =========================================================

def render_base(output, duration, vf):
    run(
        [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i",
            f"color=c=0x080808:s={W}x{H}:r={FPS}:d={duration}",
            "-vf",
            vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output)
        ]
    )
