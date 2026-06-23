#!/usr/bin/env python3
"""
create_videos.py

Scan a folder for JPG images and optional same-named .MOV sidecar audio files.
Produce an MP4 per image:
 - JPG as static video frame
 - audio from .MOV when present (normalized)
 - 0.5s fade-in and 0.5s fade-out on the video
 - output at 60 fps
 - skip if output file already exists
"""

import argparse
import subprocess
import shlex
import os
import sys
from pathlib import Path
import json

def run(cmd):
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc

def ffprobe_duration(path):
    cmd = (
        f'ffprobe -v error -select_streams v:0 -show_entries stream=duration '
        f'-of json "{path}"'
    )
    p = run(cmd)
    if p.returncode == 0 and p.stdout:
        try:
            j = json.loads(p.stdout)
            # duration may be in streams[0]["duration"] or format.duration; try fallback
            if "streams" in j and j["streams"]:
                d = j["streams"][0].get("duration")
                if d:
                    return float(d)
        except Exception:
            pass
    # fallback: try format duration
    cmd = f'ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "{path}"'
    p = run(cmd)
    if p.returncode == 0 and p.stdout.strip():
        try:
            return float(p.stdout.strip())
        except Exception:
            pass
    return None

def make_video(image_path: Path, mov_path: Path or None, out_path: Path, fps: int = 60, fade_s: float = 0.5, crf: int = 18, preset: str = "slow"):
    if out_path.exists():
        print(f"Skipping existing output {out_path}")
        return 0

    # If audio exists, determine its duration; otherwise set a default static duration (e.g., 5s)
    duration = None
    if mov_path and mov_path.exists():
        duration = ffprobe_duration(str(mov_path))
    if duration is None:
        # default duration for image-only video
        duration = 5.0

    # compute fade-out start time
    fade_out_start = max(0.0, duration - fade_s)

    # Build ffmpeg command
    # -loop 1 and -framerate create a stream of the static image at the requested fps
    # video filter applies fade in and out and ensures yuv420p for compatibility
    vf = f"fade=t=in:st=0:d={fade_s},fade=t=out:st={fade_out_start}:d={fade_s},format=yuv420p"
    # audio handling: if mov exists, apply loudnorm; otherwise generate silent audio
    if mov_path and mov_path.exists():
        # Use single-pass loudnorm with common params
        af = "loudnorm=I=-16:TP=-1.5:LRA=11"
        cmd = (
            f'ffmpeg -y -hide_banner -loglevel error -loop 1 -framerate {fps} -i "{image_path}" '
            f'-i "{mov_path}" -t {duration} -vf "{vf}" -map 0:v:0 -map 1:a:0 '
            f'-c:v libx264 -preset {preset} -crf {crf} -r {fps} -c:a aac -b:a 192k -af "{af}" '
            f'-movflags +faststart "{out_path}"'
        )
    else:
        # No audio: make silent audio track with aac so platforms expect audio
        # Use anullsrc to generate silent audio matching the duration
        cmd = (
            f'ffmpeg -y -hide_banner -loglevel error -loop 1 -framerate {fps} -i "{image_path}" '
            f'-f lavfi -t {duration} -i "anullsrc=cl=stereo:r=48000" -t {duration} '
            f'-vf "{vf}" -map 0:v:0 -map 1:a:0 '
            f'-c:v libx264 -preset {preset} -crf {crf} -r {fps} -c:a aac -b:a 128k '
            f'-movflags +faststart "{out_path}"'
        )

    print(f"Creating {out_path.name} (duration {duration:.2f}s)...")
    p = run(cmd)
    if p.returncode != 0:
        print(f"ffmpeg failed for {image_path.name}: {p.stderr}", file=sys.stderr)
        return p.returncode
    print(f"Created {out_path}")
    return 0

def find_images(folder: Path):
    exts = {'.jpg', '.jpeg', '.JPG', '.JPEG'}
    for p in folder.iterdir():
        if p.is_file() and p.suffix in exts:
            yield p

def main():
    parser = argparse.ArgumentParser(description="Create MP4 videos from JPG images and optional MOV sidecar audio.")
    parser.add_argument("input", help="Input folder containing JPG and MOV sidecar files")
    parser.add_argument("-o", "--output", default="output_videos", help="Output folder for MP4 files")
    parser.add_argument("--fps", type=int, default=60, help="Output frames per second")
    parser.add_argument("--fade", type=float, default=0.5, help="Fade-in and fade-out duration in seconds")
    parser.add_argument("--crf", type=int, default=18, help="H.264 CRF (lower = less compression, larger files)")
    parser.add_argument("--preset", default="slow", help="x264 preset (e.g., ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)")
    args = parser.parse_args()

    in_folder = Path(args.input)
    out_folder = Path(args.output)
    if not in_folder.exists() or not in_folder.is_dir():
        print("Input folder does not exist or is not a directory", file=sys.stderr)
        sys.exit(2)
    out_folder.mkdir(parents=True, exist_ok=True)

    images = sorted(find_images(in_folder))
    if not images:
        print("No JPG images found in the input folder.", file=sys.stderr)
        sys.exit(0)

    failures = 0
    for img in images:
        base = img.stem
        mov = in_folder / f"{base}.mov"
        # allow case-insensitive .MOV extension too
        if not mov.exists():
            mov_upper = in_folder / f"{base}.MOV"
            if mov_upper.exists():
                mov = mov_upper
        out_path = out_folder / f"{base}.mp4"
        rc = make_video(img, mov if mov.exists() else None, out_path, fps=args.fps, fade_s=args.fade, crf=args.crf, preset=args.preset)
        if rc != 0:
            failures += 1

    if failures:
        print(f"Completed with {failures} failures.", file=sys.stderr)
        sys.exit(1)
    print("All done.")

if __name__ == "__main__":
    main()
