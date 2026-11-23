#!/bin/bash
# usage: tools/seqstills.sh CONTENT SEQ "frames" OUTDIR
cd "$(dirname "$0")/.." && node tools/still.mjs --content "$1" --seq "$2" --frames "$3" --out "$4" --name "$2"
