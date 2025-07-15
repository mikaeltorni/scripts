"""
Losslessly cut the last 60 s of every video in the current directory.
Requires ffmpeg/ffprobe on PATH.
Outputs are saved in the 'output' subfolder.

Usage:
python main.py
"""

import os
import subprocess
import sys
from pathlib import Path

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm", ".ts", ".m4v", ".wmv"}
CUT_DURATION = 60  # seconds
OUTPUT_DIR = Path("output")

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def run(cmd: list[str]) -> str:
    """Run a shell command and return stdout as str."""
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    return proc.stdout


def get_duration(path: Path) -> float:
    """Return duration in seconds using ffprobe."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "csv=p=0",
        str(path),
    ]
    return float(run(cmd).strip())


def ffmpeg_trim_last(path: Path, duration: float) -> None:
    """Losslessly cut the last CUT_DURATION seconds and save to output subfolder."""
    start = max(duration - CUT_DURATION, 0)
    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / f"{path.stem}_cut.mp4"

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        str(start),
        "-i",
        str(path),
        "-c",
        "copy",
        "-avoid_negative_ts",
        "make_zero",
        str(out_path),
    ]
    subprocess.run(cmd, check=True)
    print(f"Saved: {out_path}")


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main() -> None:
    files = [
        Path(p)
        for p in os.listdir(".")
        if Path(p).suffix.lower() in VIDEO_EXTS and Path(p).is_file()
    ]
    if not files:
        print("No video files found in current directory.")
        sys.exit(0)

    OUTPUT_DIR.mkdir(exist_ok=True)

    for f in files:
        try:
            dur = get_duration(f)
            print(f"{f.name}: {dur:.2f} s")
            ffmpeg_trim_last(f, dur)
        except Exception as e:
            print(f"Skipping {f.name}: {e}")


if __name__ == "__main__":
    main()
