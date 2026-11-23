#!/bin/bash
Y=~/.agent-reach-venv/bin/yt-dlp
line="$1"; id="${line%%|*}"; sec="${line##*|}"
args=(-q -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 -o "src2/$id.%(ext)s")
[ -n "$sec" ] && args+=(--download-sections "$sec")
$Y --no-update "${args[@]}" "https://www.youtube.com/watch?v=$id" >/dev/null 2>&1
echo "$id $(ls src2/$id.mp4 2>/dev/null | wc -l)"
