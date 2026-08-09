import subprocess
from pathlib import Path

OUTPUT = Path("final_reel.mp4")

cmd = [
    "ffmpeg",
    "-y",

    "-f", "lavfi",
    "-i",
    "color=c=black:s=1080x1920:r=30:d=5",

    "-vf",
    (
        "drawtext="
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "text='AI IS CHANGING EVERYTHING':"
        "fontcolor=white:"
        "fontsize=82:"
        "x=(w-text_w)/2:"
        "y=(h-text_h)/2:"
        "enable='between(t,0,5)'"
    ),

    "-c:v", "libx264",
    "-preset", "veryfast",
    "-pix_fmt", "yuv420p",

    str(OUTPUT)
]

subprocess.run(cmd, check=True)

print(f"RENDER COMPLETE: {OUTPUT}")
