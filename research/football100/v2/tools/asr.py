#!/usr/bin/env python3
"""Word-level ASR of the narration voice track. Run with the kokoro venv python (has faster-whisper):
  ../video_build/kvenv/bin/python v2/tools/asr.py 001 002 ...
Writes v2/asr/NNN.json {"voice": path, "dur": seconds, "words": [{"w","s","e"}]} and v2/work/NNN/voice.wav (single voice file, Kokoro lines concatenated with 0.3 s gaps exactly like build100)."""
import glob, json, os, subprocess, sys
H = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GAP = 0.3


def voice_file(no):
    j = json.load(open(f"{H}/scripts/{no:03d}.json")); n = len(j["lines"])
    os.makedirs(f"{H}/v2/work/{no:03d}", exist_ok=True)
    out = f"{H}/v2/work/{no:03d}/voice.wav"
    if j["voice"] == "kokoro":
        if not os.path.exists(out):
            ins = sum([["-i", f"{H}/voice/{no:03d}_{i + 1}.wav"] for i in range(n)], [])
            fc = "".join(f"[{i}]apad=pad_dur={GAP}[a{i}];" for i in range(n)) + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
            subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[o]", out], check=True)
        return out
    return glob.glob(f"{H}/voice/{no:03d}_el.*")[0]


def main(nos):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=3)
    for no in nos:
        dst = f"{H}/v2/asr/{no:03d}.json"
        if os.path.exists(dst): continue
        vf = voice_file(no)
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vf, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
        import numpy as np
        audio = np.frombuffer(raw, dtype=np.float32)
        segs, info = m.transcribe(audio, language="en", word_timestamps=True, beam_size=5, vad_filter=False, condition_on_previous_text=False)
        words = []
        for s in segs:
            for w in (s.words or []): words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
        json.dump({"voice": vf, "dur": round(len(audio) / 16000, 3), "words": words}, open(dst, "w"))
        print("asr", no, len(words), "words", len(audio) / 16000, flush=True)


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]])
