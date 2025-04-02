#!/bin/sh

to_down_file="$1"
save_dir="$2"

FORMAT="bestvideo[height<=360][ext=mp4][protocol=https][acodec=none]"
merge_output_format=mp4
concurrent_fragments=8

download_archive="$save_dir/archive.txt"
output="$save_dir/%(id)s/%(id)s.%(ext)s"

yt-dlp \
    -f "$FORMAT" \
    -o "$output" \
    --write-info-json \
    -N "$concurrent_fragments" \
    --download-archive "$download_archive" \
    --merge-output-format "$merge_output_format" \
    -a "$to_down_file"