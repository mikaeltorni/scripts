# ffmpeg_video_cutter

Losslessly extract the last 60 s of every video in the current directory.

## Usage
```bash
python3 ffmpeg_video_cutter.py
```

## Requirements
- Python 3
- `ffmpeg` and `ffprobe` on PATH

## Supported extensions
.mp4 .mkv .mov .avi .flv .webm .ts .m4v .wmv

## Output
`filename_cut.mp4` next to each source file, no re-encode (stream-copy).
