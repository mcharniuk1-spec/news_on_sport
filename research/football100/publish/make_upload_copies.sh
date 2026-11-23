#!/bin/bash
# <10 MB copies for the browser file-upload tool (full-quality masters stay in FINAL_100_v2/videos)
cd "$(dirname "$0")/.."; mkdir -p publish/upload
one(){ n=$1; out=publish/upload/$n.mp4; [ -f "$out" ] && exit 0; f=$(ls FINAL_100_v2/videos/${n}_*.mp4); d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"); vb=$(python3 -c "print(int((9.2e6*8/$d - 112000)/1000))"); ffmpeg -v error -y -i "$f" -c:v libx264 -preset slow -b:v ${vb}k -maxrate $((vb*13/10))k -bufsize $((vb*2))k -profile:v high -pix_fmt yuv420p -g 60 -c:a aac -b:a 96k -ar 44100 -movflags +faststart "$out"; }
export -f one
seq -f "%03g" 1 100 | xargs -P 4 -I{} bash -c 'one {}'
