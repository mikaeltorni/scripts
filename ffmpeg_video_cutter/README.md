# cut_last_minute.py

Losslessly extract the last 60 s of every video in the current directory.

## Usage
```bash
python3 cut_last_minute.py
```

## Requirements
- Python 3
- `ffmpeg` and `ffprobe` on PATH

## Supported extensions
.mp4 .mkv .mov .avi .flv .webm .ts .m4v .wmv

## Output
`filename_cut.mp4` next to each source file, no re-encode (stream-copy).
