import subprocess
from pathlib import Path

W = 1080
H = 1920
FPS = 30

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def run(cmd):
    print("\nGRAPHICS:", " ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


def esc(text):
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace(",", "\\,")
    )


def base_input(duration, background="0x080808"):
    return [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c={background}:s={W}x{H}:r={FPS}:d={duration}",
    ]


def encode(output):
    return [
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-an",
        str(output),
    ]


# =========================================================
# 1. TITLE / HOOK
# =========================================================

def render_hook(output, duration):
    text = esc("AI IS CHANGING EVERYTHING")

    vf = (
        f"drawtext=fontfile={FONT_BOLD}:"
        f"text='{text}':"
        "fontcolor=white:"
        "fontsize=82:"
        "x=(w-text_w)/2:"
        "y=(h-text_h)/2:"
        "alpha='if(lt(t,0.25),t/0.25,1)':"
        "enable='between(t,0,1.3)'"
    )

    run(
        base_input(duration, "0x050505")
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 2. WORKFLOW GRAPHIC
# =========================================================

def render_workflow(output, duration):
    vf = (
        "drawbox=x=90:y=500:w=900:h=820:"
        "color=0x111111:t=fill,"
        "drawbox=x=130:y=560:w=220:h=180:"
        "color=0x1C1C1C:t=fill,"
        "drawbox=x=430:y=560:w=220:h=180:"
        "color=0x1C1C1C:t=fill,"
        "drawbox=x=730:y=560:w=220:h=180:"
        "color=0x1C1C1C:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='RESEARCH':"
        "fontcolor=white:"
        "fontsize=42:"
        "x=155:y=625,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='CREATE':"
        "fontcolor=white:"
        "fontsize=42:"
        "x=475:y=625,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='PUBLISH':"
        "fontcolor=white:"
        "fontsize=42:"
        "x=765:y=625,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='AI WORKFLOW':"
        "fontcolor=0xBBBBBB:"
        "fontsize=38:"
        "x=(w-text_w)/2:"
        "y=430,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='AUTOMATED':"
        "fontcolor=white:"
        "fontsize=70:"
        "x=(w-text_w)/2:"
        "y=1050"
    )

    run(
        base_input(duration, "0x080808")
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 3. RESEARCH CARD
# =========================================================

def render_research(output, duration):
    vf = (
        "drawbox=x=150:y=550:w=780:h=650:"
        "color=0x111111:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='01':"
        "fontcolor=0x777777:"
        "fontsize=42:"
        "x=200:y=620,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='RESEARCH':"
        "fontcolor=white:"
        "fontsize=78:"
        "x=200:y=730,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='AI finds the information':"
        "fontcolor=0xBBBBBB:"
        "fontsize=38:"
        "x=200:y=850,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='you need.':"
        "fontcolor=0xBBBBBB:"
        "fontsize=38:"
        "x=200:y=910"
    )

    run(
        base_input(duration)
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 4. CREATE CARD
# =========================================================

def render_create(output, duration):
    vf = (
        "drawbox=x=150:y=550:w=780:h=650:"
        "color=0x111111:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='02':"
        "fontcolor=0x777777:"
        "fontsize=42:"
        "x=200:y=620,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='CREATE':"
        "fontcolor=white:"
        "fontsize=78:"
        "x=200:y=730,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='Scripts, visuals,':"
        "fontcolor=0xBBBBBB:"
        "fontsize=38:"
        "x=200:y=850,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='and content generated.':"
        "fontcolor=0xBBBBBB:"
        "fontsize=38:"
        "x=200:y=910"
    )

    run(
        base_input(duration)
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 5. PUBLISH CARD
# =========================================================

def render_publish(output, duration):
    vf = (
        "drawbox=x=150:y=550:w=780:h=650:"
        "color=0x111111:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='03':"
        "fontcolor=0x777777:"
        "fontsize=42:"
        "x=200:y=620,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='PUBLISH':"
        "fontcolor=white:"
        "fontsize=78:"
        "x=200:y=730,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='Ready for the audience.':"
        "fontcolor=0xBBBBBB:"
        "fontsize=38:"
        "x=200:y=870"
    )

    run(
        base_input(duration)
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 6. AUTOMATION CARD
# =========================================================

def render_automation(output, duration):
    vf = (
        "drawbox=x=120:y=520:w=840:h=820:"
        "color=0x101010:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='AUTOMATION':"
        "fontcolor=white:"
        "fontsize=76:"
        "x=(w-text_w)/2:"
        "y=650,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='ONE WORKFLOW':"
        "fontcolor=0xAAAAAA:"
        "fontsize=42:"
        "x=(w-text_w)/2:"
        "y=800,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='MANY TASKS':"
        "fontcolor=white:"
        "fontsize=62:"
        "x=(w-text_w)/2:"
        "y=920"
    )

    run(
        base_input(duration)
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 7. CUTS
# =========================================================

def render_cuts(output, duration):
    vf = (
        "drawbox=x=180:y=600:w=720:h=500:"
        "color=0x111111:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='CUTS':"
        "fontcolor=white:"
        "fontsize=100:"
        "x=(w-text_w)/2:"
        "y=760"
    )

    run(
        base_input(duration)
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 8. CAPTIONS
# =========================================================

def render_captions(output, duration):
    vf = (
        "drawbox=x=120:y=560:w=840:h=650:"
        "color=0x111111:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='CAPTIONS':"
        "fontcolor=white:"
        "fontsize=78:"
        "x=(w-text_w)/2:"
        "y=720,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='GENERATED AUTOMATICALLY':"
        "fontcolor=0xAAAAAA:"
        "fontsize=36:"
        "x=(w-text_w)/2:"
        "y=850"
    )

    run(
        base_input(duration)
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 9. FULL AUTOMATION / TIMELINE
# =========================================================

def render_timeline(output, duration):
    vf = (
        "drawbox=x=100:y=500:w=880:h=850:"
        "color=0x101010:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='CUTS + CAPTIONS + SCORES':"
        "fontcolor=white:"
        "fontsize=54:"
        "x=(w-text_w)/2:"
        "y=670,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='AUTOMATICALLY':"
        "fontcolor=white:"
        "fontsize=76:"
        "x=(w-text_w)/2:"
        "y=820,"
        f"drawtext=fontfile={FONT_REGULAR}:"
        "text='FROM ONE WORKFLOW':"
        "fontcolor=0xAAAAAA:"
        "fontsize=38:"
        "x=(w-text_w)/2:"
        "y=960"
    )

    run(
        base_input(duration)
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 10. DASHBOARD
# =========================================================

def render_dashboard(output, duration):
    vf = (
        "drawbox=x=120:y=500:w=840:h=850:"
        "color=0x101010:t=fill,"
        "drawbox=x=190:y=850:w=170:h=250:"
        "color=0x222222:t=fill,"
        "drawbox=x=410:y=700:w=170:h=400:"
        "color=0x222222:t=fill,"
        "drawbox=x=630:y=590:w=170:h=510:"
        "color=0x222222:t=fill,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='OUTPUT':"
        "fontcolor=white:"
        "fontsize=70:"
        "x=(w-text_w)/2:"
        "y=570"
    )

    run(
        base_input(duration)
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# 11. FINAL PUNCH
# =========================================================

def render_final(output, duration):
    vf = (
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='AUTOMATE MORE.':"
        "fontcolor=white:"
        "fontsize=82:"
        "x=(w-text_w)/2:"
        "y=780,"
        f"drawtext=fontfile={FONT_BOLD}:"
        "text='CREATE MORE.':"
        "fontcolor=white:"
        "fontsize=82:"
        "x=(w-text_w)/2:"
        "y=900"
    )

    run(
        base_input(duration, "0x050505")
        + ["-vf", vf]
        + encode(output)
    )


# =========================================================
# MAIN DISPATCHER
# =========================================================

def render_graphic(output, shot):

    shot_id = int(shot["id"])
    duration = float(shot["duration"])

    graphic = shot.get("graphic", "")

    if graphic == "hook":
        render_hook(output, duration)

    elif graphic == "workflow":
        render_workflow(output, duration)

    elif graphic == "research":
        render_research(output, duration)

    elif graphic == "create":
        render_create(output, duration)

    elif graphic == "publish":
        render_publish(output, duration)

    elif graphic == "automation":
        render_automation(output, duration)

    elif graphic == "cuts":
        render_cuts(output, duration)

    elif graphic == "captions":
        render_captions(output, duration)

    elif graphic == "timeline":
        render_timeline(output, duration)

    elif graphic == "dashboard":
        render_dashboard(output, duration)

    elif graphic == "final":
        render_final(output, duration)

    else:
        # Safe fallback
        render_hook(output, duration)
