import subprocess
from pathlib import Path

# ============================================================
# REEL FACTORY — MOTION GRAPHICS ENGINE V3
# ------------------------------------------------------------
# Reusable FFmpeg motion-graphics scenes.
# No per-reel animation code is required.
# Timeline selects a scene; this file renders it.
# ============================================================

W = 1080
H = 1920
FPS = 30

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = "0x07090D"
PANEL = "0x0D1118"
CARD = "0x121923"
CARD_2 = "0x17212D"
WHITE = "0xF5F7FA"
MUTED = "0x8D9AA8"
ACCENT = "0x35E6FF"
ACCENT_2 = "0x7A5CFF"
GREEN = "0x45E0A6"
RED = "0xFF5C7A"


def run(cmd):
    print("\nGRAPHICS RUNNING:")
    print(" ".join(str(x) for x in cmd))
    subprocess.run(["ffmpeg"] + [str(x) for x in cmd], check=True)


def base_input(duration):
    return [
        "-y",
        "-f", "lavfi",
        "-i", f"color=c={BG}:s={W}x{H}:r={FPS}:d={duration}",
    ]


def render(output, duration, vf):
    run(
        base_input(duration)
        + [
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output),
        ]
    )


def text(value):
    return (
        str(value)
        .replace("\\", "")
        .replace("'", r"\'")
        .replace(":", r"\:")
        .replace(",", r"\,")
        .replace("%", r"\%")
    )


# ============================================================
# Shared animated background
# ============================================================

def background_layers():
    return (
        "drawbox=x=0:y=0:w=1080:h=1920:color=0x07090D:t=fill,"
        # top glow bands
        "drawbox=x=-120:y=260:w=520:h=520:color=0x101B2A:t=fill,"
        "drawbox=x=680:y=1120:w=560:h=560:color=0x0D1824:t=fill,"
        # subtle animated scan line
        "drawbox="
        "x=0:"
        "y='mod(t*170,1920)':"
        "w=1080:h=2:"
        "color=0x13202B:t=fill:"
        "enable='lt(mod(t,2.8),1.4)',"
    )


# ============================================================
# 1. HOOK — kinetic typography
# ============================================================

def render_hook(output, duration, title="AUTOMATE."):
    s = text(title)

    vf = (
        background_layers()
        + f"drawbox="
          f"x='540-(80+min(430,t*900))':"
          f"y=956:"
          f"w='2*(80+min(430,t*900))':"
          f"h=5:"
          f"color={ACCENT}:t=fill,"
        f"drawtext="
        f"fontfile={FONT}:"
        f"text='{s}':"
        f"fontcolor={WHITE}:"
        f"fontsize='min(150,70+t*220)':"
        f"x='(w-text_w)/2':"
        f"y='(h-text_h)/2':"
        f"alpha='min(1,t*5)':"
        f"shadowcolor=black@0.45:"
        f"shadowx=0:"
        f"shadowy=8,"
        f"drawtext="
        f"fontfile={FONT_REGULAR}:"
        f"text='AI REEL FACTORY':"
        f"fontcolor={MUTED}:"
        f"fontsize=28:"
        f"x='(w-text_w)/2':"
        f"y=1040:"
        f"alpha='max(0,min(1,(t-0.35)*4))'"
    )

    render(output, duration, vf)


# ============================================================
# 2. WORKFLOW — nodes physically enter + connectors grow
# ============================================================

def render_workflow(output, duration):
    vf = (
        background_layers()
        # panel
        + f"drawbox=x=70:y=420:w=940:h=1060:color={PANEL}:t=fill,"
        f"drawbox=x=70:y=420:w=940:h=4:color={ACCENT}:t=fill,"
        # connector 1
        "drawbox="
        "x=300:y=730:"
        "w='max(0,min(230,(t-0.45)*460))':"
        "h=6:"
        f"color={ACCENT}:t=fill,"
        # connector 2
        "drawbox="
        "x=550:y=730:"
        "w='max(0,min(230,(t-0.95)*460))':"
        "h=6:"
        f"color={ACCENT}:t=fill,"
        # node 1 slides from left
        f"drawbox="
        f"x='120-max(0,min(230,(t-0.1)*460))':"
        f"y=650:w=230:h=160:color={CARD}:t=fill,"
        # node 2 slides from top
        f"drawbox="
        f"x=425:"
        f"y='650-max(0,min(160,(t-0.55)*460))':"
        f"w=230:h=160:color={CARD_2}:t=fill,"
        # node 3 slides from right
        f"drawbox="
        f"x='730+max(0,min(230,(t-1.0)*460))':"
        f"y=650:w=230:h=160:color={CARD}:t=fill,"
        # labels
        f"drawtext=fontfile={FONT_REGULAR}:text='INPUT':fontcolor={MUTED}:fontsize=30:x=180:y=690:alpha='min(1,t*5)',"
        f"drawtext=fontfile={FONT}:text='AI':fontcolor={ACCENT}:fontsize=58:x='(w-text_w)/2':y=700:alpha='max(0,min(1,(t-0.55)*5))',"
        f"drawtext=fontfile={FONT_REGULAR}:text='OUTPUT':fontcolor={MUTED}:fontsize=30:x=765:y=690:alpha='max(0,min(1,(t-1.0)*5))',"
        # lower task cards
        f"drawbox=x=140:y=930:w=800:h=90:color={CARD}:t=fill:"
        f"enable='gte(t,1.15)',"
        f"drawtext=fontfile={FONT_REGULAR}:text='RESEARCH   →   CREATE   →   PUBLISH':fontcolor={WHITE}:fontsize=34:x='(w-text_w)/2':y=958:alpha='max(0,min(1,(t-1.15)*4))',"
        # headline
        f"drawtext=fontfile={FONT}:text='ONE WORKFLOW. MANY TASKS.':fontcolor={WHITE}:fontsize=54:x='(w-text_w)/2':y=1110:alpha='max(0,min(1,(t-1.35)*4))',"
        f"drawtext=fontfile={FONT_REGULAR}:text='AUTOMATION RUNNING':fontcolor={ACCENT}:fontsize=27:x='(w-text_w)/2':y=1190:alpha='max(0,min(1,(t-1.7)*4))'"
    )
    render(output, duration, vf)


# ============================================================
# 3. AI AGENT PIPELINE — animated process diagram
# ============================================================

def render_agent_pipeline(output, duration):
    vf = (
        background_layers()
        + f"drawbox=x=90:y=390:w=900:h=1170:color={PANEL}:t=fill,"
        # central card grows
        f"drawbox="
        f"x='540-(120+min(320,t*700))':"
        f"y='780-(90+min(150,t*300))':"
        f"w='2*(120+min(320,t*700))':"
        f"h='2*(90+min(150,t*300))':"
        f"color={CARD}:t=fill,"
        # pulse bars
        f"drawbox=x=245:y=600:w='min(590,max(0,(t-0.2)*800))':h=5:color={ACCENT}:t=fill,"
        # three process steps
        f"drawtext=fontfile={FONT}:text='THINK':fontcolor={WHITE}:fontsize=52:x='(w-text_w)/2':y=700:alpha='max(0,min(1,(t-0.35)*6))',"
        f"drawtext=fontfile={FONT}:text='DECIDE':fontcolor={WHITE}:fontsize=52:x='(w-text_w)/2':y=805:alpha='max(0,min(1,(t-0.65)*6))',"
        f"drawtext=fontfile={FONT}:text='EXECUTE':fontcolor={ACCENT}:fontsize=52:x='(w-text_w)/2':y=910:alpha='max(0,min(1,(t-0.95)*6))',"
        # side nodes
        f"drawbox=x=150:y=1040:w=250:h=90:color={CARD_2}:t=fill:enable='gte(t,1.1)',"
        f"drawbox=x=680:y=1040:w=250:h=90:color={CARD_2}:t=fill:enable='gte(t,1.35)',"
        f"drawtext=fontfile={FONT_REGULAR}:text='TOOLS':fontcolor={MUTED}:fontsize=28:x=235:y=1072:alpha='max(0,min(1,(t-1.1)*5))',"
        f"drawtext=fontfile={FONT_REGULAR}:text='RESULT':fontcolor={GREEN}:fontsize=28:x=745:y=1072:alpha='max(0,min(1,(t-1.35)*5))',"
        # arrows
        f"drawbox=x=400:y=1080:w='max(0,min(280,(t-1.3)*500))':h=5:color={ACCENT}:t=fill,"
        f"drawtext=fontfile={FONT}:text='AI AGENT':fontcolor={ACCENT}:fontsize=32:x='(w-text_w)/2':y=520:alpha='min(1,t*5)'"
    )
    render(output, duration, vf)


# ============================================================
# 4. TIMELINE — animated editor-like sequence
# ============================================================

def render_timeline(output, duration):
    vf = (
        background_layers()
        + f"drawbox=x=65:y=470:w=950:h=1030:color={PANEL}:t=fill,"
        # header
        f"drawtext=fontfile={FONT}:text='AUTOMATED TIMELINE':fontcolor={WHITE}:fontsize=58:x=120:y=560:alpha='min(1,t*4)',"
        f"drawtext=fontfile={FONT_REGULAR}:text='CREATE   /   PROCESS   /   PUBLISH':fontcolor={MUTED}:fontsize=28:x=120:y=635:alpha='max(0,min(1,(t-0.3)*4))',"
        # tracks
        f"drawbox=x=130:y=780:w=820:h=100:color={CARD}:t=fill,"
        f"drawbox=x=130:y=910:w=820:h=100:color={CARD}:t=fill,"
        f"drawbox=x=130:y=1040:w=820:h=100:color={CARD}:t=fill,"
        # moving clips
        f"drawbox=x=160:y=800:w='min(260,max(20,t*360))':h=60:color={ACCENT}:t=fill,"
        f"drawbox=x='400+max(0,min(220,(t-0.55)*300))':y=930:w=210:h=60:color={ACCENT_2}:t=fill,"
        f"drawbox=x='620+max(0,min(130,(t-1.05)*250))':y=1060:w=170:h=60:color={GREEN}:t=fill,"
        # playhead
        f"drawbox=x='150+min(800,(t/3.2)*800)':y=750:w=5:h=420:color={WHITE}:t=fill,"
        # labels
        f"drawtext=fontfile={FONT_REGULAR}:text='VIDEO':fontcolor={MUTED}:fontsize=24:x=150:y=760,"
        f"drawtext=fontfile={FONT_REGULAR}:text='AI':fontcolor={MUTED}:fontsize=24:x=150:y=890,"
        f"drawtext=fontfile={FONT_REGULAR}:text='OUTPUT':fontcolor={MUTED}:fontsize=24:x=150:y=1020,"
        f"drawtext=fontfile={FONT}:text='AUTO-EDITING':fontcolor={ACCENT}:fontsize=40:x='(w-text_w)/2':y=1260:alpha='max(0,min(1,(t-1.1)*4))'"
    )
    render(output, duration, vf)


# ============================================================
# 5. DASHBOARD — animated KPI cards + bars
# ============================================================

def render_dashboard(output, duration):
    vf = (
        background_layers()
        + f"drawbox=x=65:y=410:w=950:h=1140:color={PANEL}:t=fill,"
        f"drawtext=fontfile={FONT}:text='AUTOMATION DASHBOARD':fontcolor={WHITE}:fontsize=52:x=110:y=510:alpha='min(1,t*4)',"
        # KPI cards
        f"drawbox=x=110:y=590:w=260:h=220:color={CARD}:t=fill,"
        f"drawbox=x=410:y=590:w=260:h=220:color={CARD}:t=fill,"
        f"drawbox=x=710:y=590:w=260:h=220:color={CARD}:t=fill,"
        f"drawtext=fontfile={FONT}:text='87 PCT':fontcolor={ACCENT}:fontsize=62:x=185:y=650:alpha='min(1,t*5)',"
        f"drawtext=fontfile={FONT}:text='42':fontcolor={WHITE}:fontsize=62:x=505:y=650:alpha='max(0,min(1,(t-.35)*5))',"
        f"drawtext=fontfile={FONT}:text='24/7':fontcolor={GREEN}:fontsize=62:x=775:y=650:alpha='max(0,min(1,(t-.7)*5))',"
        f"drawtext=fontfile={FONT_REGULAR}:text='AUTOMATED':fontcolor={MUTED}:fontsize=24:x=165:y=735,"
        f"drawtext=fontfile={FONT_REGULAR}:text='TASKS':fontcolor={MUTED}:fontsize=24:x=510:y=735,"
        f"drawtext=fontfile={FONT_REGULAR}:text='RUNNING':fontcolor={MUTED}:fontsize=24:x=765:y=735,"
        # graph area
        f"drawbox=x=110:y=900:w=860:h=450:color={CARD}:t=fill,"
        f"drawbox=x=160:y=1250:w='min(740,max(0,(t-0.5)*330))':h=8:color={ACCENT}:t=fill,"
        f"drawbox=x=160:y=1190:w='min(620,max(0,(t-0.8)*300))':h=8:color={ACCENT_2}:t=fill,"
        f"drawbox=x=160:y=1130:w='min(500,max(0,(t-1.1)*270))':h=8:color={GREEN}:t=fill,"
        f"drawtext=fontfile={FONT_REGULAR}:text='OUTPUT':fontcolor={MUTED}:fontsize=25:x=160:y=1070:alpha='max(0,min(1,(t-.4)*4))'"
    )
    render(output, duration, vf)


# ============================================================
# 6. CHAPTER / PAYOFF
# ============================================================

def render_chapter(output, duration, title="PUBLISH"):
    s = text(title)
    vf = (
        background_layers()
        + f"drawbox="
          f"x='540-(40+min(420,t*900))':"
          f"y=1080:"
          f"w='2*(40+min(420,t*900))':"
          f"h=5:"
          f"color={ACCENT}:t=fill,"
        f"drawtext=fontfile={FONT}:text='{s}':fontcolor={WHITE}:fontsize='min(145,55+t*250)':x='(w-text_w)/2':y='(h-text_h)/2':alpha='min(1,t*5)',"
        f"drawtext=fontfile={FONT_REGULAR}:text='FROM IDEA TO OUTPUT':fontcolor={MUTED}:fontsize=30:x='(w-text_w)/2':y=1120:alpha='max(0,min(1,(t-.45)*4))'"
    )
    render(output, duration, vf)


# ============================================================
# 7. DISPATCHER
# ============================================================

def render_graphic(output, shot):
    duration = float(shot["duration"])
    graphic = shot.get("graphic", "placeholder")

    print(f"GRAPHIC ENGINE V3 → {graphic}")

    if graphic == "hook":
        render_hook(output, duration, shot.get("text", "AUTOMATE."))
    elif graphic == "workflow":
        render_workflow(output, duration)
    elif graphic == "agent_pipeline":
        render_agent_pipeline(output, duration)
    elif graphic == "timeline":
        render_timeline(output, duration)
    elif graphic == "dashboard":
        render_dashboard(output, duration)
    elif graphic == "chapter":
        render_chapter(output, duration, shot.get("title", "PUBLISH"))
    else:
        render_hook(output, duration, f"SHOT {shot.get('id', '?')}")
