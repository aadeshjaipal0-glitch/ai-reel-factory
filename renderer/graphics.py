import subprocess
from pathlib import Path


# ============================================================
# REEL FACTORY — PREMIUM MOTION GRAPHICS ENGINE V2
# ============================================================

W = 1080
H = 1920
FPS = 30

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


# ============================================================
# COMMAND RUNNER
# ============================================================

def run(cmd):
    print("\nGRAPHICS RUNNING:")
    print(" ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


# ============================================================
# COMMON FFMPEG FILTERS
# ============================================================

def base_input(duration):
    return [
        "-y",
        "-f", "lavfi",
        "-i",
        f"color=c=0x07090D:s={W}x{H}:r={FPS}:d={duration}"
    ]


# ============================================================
# 1. PREMIUM HOOK
# ============================================================

def render_hook(output, duration, text="AUTOMATE."):
    safe = text.replace("'", r"\'")

    vf = (
        f"drawtext="
        f"fontfile={FONT}:"
        f"text='{safe}':"
        f"fontcolor=white:"
        f"fontsize=120:"
        f"x=(w-text_w)/2:"
        f"y=(h-text_h)/2:"
        f"alpha='min(1,t*5)':"
        f"enable='between(t,0,{duration})'"
        ","
        "drawbox="
        "x=100:y=940:"
        "w=880:h=4:"
        "color=0x35E6FF:"
        "t=fill:"
        "enable='between(t,0.15,1.0)'"
    )

    run(
        base_input(duration)
        + [
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output)
        ]
    )


# ============================================================
# 2. ANIMATED WORKFLOW
# ============================================================

def render_workflow(output, duration):
    vf = (
        # background glow
        "drawbox="
        "x=120:y=500:w=840:h=900:"
        "color=0x0D1118:"
        "t=fill,"
        
        # NODE 1
        "drawbox="
        "x=130:y=650:w=230:h=130:"
        "color=0x151C27:"
        "t=fill:"
        "enable='gte(t,0.2)',"

        # NODE 2
        "drawbox="
        "x=425:y=650:w=230:h=130:"
        "color=0x151C27:"
        "t=fill:"
        "enable='gte(t,0.7)',"

        # NODE 3
        "drawbox="
        "x=720:y=650:w=230:h=130:"
        "color=0x151C27:"
        "t=fill:"
        "enable='gte(t,1.2)',"

        # connector lines
        "drawbox="
        "x=360:y=710:w=65:h=6:"
        "color=0x35E6FF:"
        "t=fill:"
        "enable='gte(t,0.8)',"

        "drawbox="
        "x=655:y=710:w=65:h=6:"
        "color=0x35E6FF:"
        "t=fill:"
        "enable='gte(t,1.3)',"

        # labels
        f"drawtext="
        f"fontfile={FONT}:"
        "text='INPUT':"
        "fontcolor=white:"
        "fontsize=42:"
        "x=190:y=690:"
        "alpha='min(1,t*4)':"

        f"drawtext="
        f"fontfile={FONT}:"
        "text='AI':"
        "fontcolor=0x35E6FF:"
        "fontsize=55:"
        "x=505:y=680:"
        "alpha='max(0,min(1,(t-0.5)*4))':"

        f"drawtext="
        f"fontfile={FONT}:"
        "text='OUTPUT':"
        "fontcolor=white:"
        "fontsize=42:"
        "x=755:y=690:"
        "alpha='max(0,min(1,(t-1)*4))':"

        # bottom headline
        f"drawtext="
        f"fontfile={FONT}:"
        "text='ONE WORKFLOW. MANY TASKS.':"
        "fontcolor=white:"
        "fontsize=58:"
        "x=(w-text_w)/2:"
        "y=1120:"
        "alpha='max(0,min(1,(t-1.4)*3))'"
    )

    run(
        base_input(duration)
        + [
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output)
        ]
    )


# ============================================================
# 3. AI AGENT PIPELINE
# ============================================================

def render_agent_pipeline(output, duration):
    vf = (
        # central panel
        "drawbox="
        "x=100:y=420:w=880:h=1080:"
        "color=0x0D1118:"
        "t=fill,"

        # agent core
        "drawbox="
        "x=300:y=650:w=480:h=300:"
        "color=0x151C27:"
        "t=fill:"
        "enable='gte(t,0.3)',"

        # outer glow style lines
        "drawbox="
        "x=300:y=650:w=480:h=5:"
        "color=0x35E6FF:"
        "t=fill:"
        "enable='gte(t,0.5)',"

        # top label
        f"drawtext="
        f"fontfile={FONT}:"
        "text='AI AGENT':"
        "fontcolor=0x35E6FF:"
        "fontsize=75:"
        "x=(w-text_w)/2:"
        "y=535:"
        "alpha='min(1,t*4)',"

        # core
        f"drawtext="
        f"fontfile={FONT}:"
        "text='THINK':"
        "fontcolor=white:"
        "fontsize=55:"
        "x=(w-text_w)/2:"
        "y=720:"
        "alpha='max(0,min(1,(t-0.5)*4))',"

        f"drawtext="
        f"fontfile={FONT}:"
        "text='DECIDE':"
        "fontcolor=white:"
        "fontsize=55:"
        "x=(w-text_w)/2:"
        "y=810:"
        "alpha='max(0,min(1,(t-0.9)*4))',"

        f"drawtext="
        f"fontfile={FONT}:"
        "text='EXECUTE':"
        "fontcolor=0x35E6FF:"
        "fontsize=55:"
        "x=(w-text_w)/2:"
        "y=900:"
        "alpha='max(0,min(1,(t-1.3)*4))',"

        # output
        f"drawtext="
        f"fontfile={FONT}:"
        "text='AUTOMATION':"
        "fontcolor=white:"
        "fontsize=62:"
        "x=(w-text_w)/2:"
        "y=1120:"
        "alpha='max(0,min(1,(t-1.7)*3))'"
    )

    run(
        base_input(duration)
        + [
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output)
        ]
    )


# ============================================================
# 4. TIMELINE / AUTOMATION
# ============================================================

def render_timeline(output, duration):
    vf = (
        # panel
        "drawbox="
        "x=90:y=500:w=900:h=900:"
        "color=0x0D1118:"
        "t=fill,"

        # timeline line
        "drawbox="
        "x=160:y=950:w=760:h=8:"
        "color=0x26313D:"
        "t=fill,"

        # progress line
        "drawbox="
        "x=160:y=950:"
        "w='min(760,max(0,(t/3.5)*760))':"
        "h=8:"
        "color=0x35E6FF:"
        "t=fill,"

        # timeline nodes
        "drawbox="
        "x=200:y=920:w=60:h=60:"
        "color=0x35E6FF:"
        "t=fill:"
        "enable='gte(t,0.3)',"

        "drawbox="
        "x=470:y=920:w=60:h=60:"
        "color=0x35E6FF:"
        "t=fill:"
        "enable='gte(t,1.0)',"

        "drawbox="
        "x=740:y=920:w=60:h=60:"
        "color=0x35E6FF:"
        "t=fill:"
        "enable='gte(t,1.7)',"

        # headline
        f"drawtext="
        f"fontfile={FONT}:"
        "text='AUTOMATED TIMELINE':"
        "fontcolor=white:"
        "fontsize=72:"
        "x=(w-text_w)/2:"
        "y=650:"
        "alpha='min(1,t*3)',"

        f"drawtext="
        f"fontfile={FONT}:"
        "text='CREATE  →  PROCESS  →  PUBLISH':"
        "fontcolor=white:"
        "fontsize=43:"
        "x=(w-text_w)/2:"
        "y=1080:"
        "alpha='max(0,min(1,(t-1)*3))'"
    )

    run(
        base_input(duration)
        + [
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output)
        ]
    )


# ============================================================
# 5. DASHBOARD
# ============================================================

def render_dashboard(output, duration):
    vf = (
        "drawbox="
        "x=80:y=430:w=920:h=1100:"
        "color=0x0D1118:"
        "t=fill,"

        # cards
        "drawbox="
        "x=130:y=560:w=250:h=220:"
        "color=0x151C27:"
        "t=fill:"

        "drawbox="
        "x=415:y=560:w=250:h=220:"
        "color=0x151C27:"
        "t=fill:"

        "drawbox="
        "x=700:y=560:w=250:h=220:"
        "color=0x151C27:"
        "t=fill:"

        # values
        f"drawtext="
        f"fontfile={FONT}:"
        "text='87%':"
        "fontcolor=0x35E6FF:"
        "fontsize=65:"
        "x=195:y=635:"
        "alpha='min(1,t*4)',"

        f"drawtext="
        f"fontfile={FONT}:"
        "text='42':"
        "fontcolor=white:"
        "fontsize=65:"
        "x=505:y=635:"
        "alpha='max(0,min(1,(t-0.4)*4))',"

        f"drawtext="
        f"fontfile={FONT}:"
        "text='24/7':"
        "fontcolor=0x35E6FF:"
        "fontsize=65:"
        "x=775:y=635:"
        "alpha='max(0,min(1,(t-0.8)*4))',"

        # labels
        f"drawtext="
        f"fontfile={FONT_REGULAR}:"
        "text='AUTOMATED':"
        "fontcolor=white:"
        "fontsize=30:"
        "x=185:y=720:',"

        f"drawtext="
        f"fontfile={FONT_REGULAR}:"
        "text='TASKS':"
        "fontcolor=white:"
        "fontsize=30:"
        "x=505:y=720:",

        f"drawtext="
        f"fontfile={FONT_REGULAR}:"
        "text='RUNNING':"
        "fontcolor=white:"
        "fontsize=30:"
        "x=775:y=720:",

        # title
        f"drawtext="
        f"fontfile={FONT}:"
        "text='AUTOMATION DASHBOARD':"
        "fontcolor=white:"
        "fontsize=62:"
        "x=(w-text_w)/2:"
        "y=920:"
        "alpha='max(0,min(1,(t-1)*3))'"
    )

    run(
        base_input(duration)
        + [
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output)
        ]
    )


# ============================================================
# 6. CHAPTER CARD
# ============================================================

def render_chapter(output, duration, title):
    safe = title.replace("'", r"\'")

    vf = (
        f"drawtext="
        f"fontfile={FONT}:"
        f"text='{safe}':"
        "fontcolor=white:"
        "fontsize=130:"
        "x=(w-text_w)/2:"
        "y=(h-text_h)/2:"
        "alpha='min(1,t*4)'"
        ","
        "drawbox="
        "x=160:y=1040:w=760:h=5:"
        "color=0x35E6FF:"
        "t=fill:"
        "enable='gte(t,0.5)'"
    )

    run(
        base_input(duration)
        + [
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output)
        ]
    )


# ============================================================
# 7. GENERIC PLACEHOLDER
# ============================================================

def render_placeholder(output, duration, text):
    safe = text.replace("'", r"\'")

    vf = (
        f"drawtext="
        f"fontfile={FONT}:"
        f"text='{safe}':"
        "fontcolor=white:"
        "fontsize=70:"
        "x=(w-text_w)/2:"
        "y=(h-text_h)/2"
    )

    run(
        base_input(duration)
        + [
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output)
        ]
    )


# ============================================================
# MAIN DISPATCHER
# ============================================================

def render_graphic(output, shot):
    duration = float(shot["duration"])
    graphic = shot.get("graphic", "placeholder")

    print(f"GRAPHIC ENGINE V2 → {graphic}")

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

    elif graphic == "agent_pipeline":
        render_agent_pipeline(
            output,
            duration
        )

    elif graphic == "timeline":
        render_timeline(
            output,
            duration
        )

    elif graphic == "dashboard":
        render_dashboard(
            output,
            duration
        )

    elif graphic == "chapter":
        render_chapter(
            output,
            duration,
            shot.get("title", "PUBLISH")
        )

    else:
        render_placeholder(
            output,
            duration,
            f"SHOT {shot.get('id', '?')}"
        )
