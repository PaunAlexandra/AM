# whisperx_script.py
import json
import sys
import whisperx

def jaccard_similarity(sent1, sent2):
    token1 = set(sent1.lower().split())
    token2 = set(sent2.lower().split())
    return float(len(token1 & token2) / len(token1 | token2)) if token1 | token2 else 0.0

def sincronizeaza_versuri_whisperx(audio_path, lyrics_path, output_sync_map, model_lang='en'):
    model = whisperx.load_model("large-v2", device="cpu", compute_type="int8")
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, language=model_lang)

    model_a, metadata = whisperx.load_align_model(language_code=model_lang, device="cpu")
    result_aligned = whisperx.align(result["segments"], model_a, metadata, audio, device="cpu")

    with open(lyrics_path, 'r') as f:
        lyrics_lines = [line.strip() for line in f if line.strip()]

    fragments = []
    lyrics_left = lyrics_lines.copy()

    for segment in result_aligned["segments"]:
        best_sim = 0.0
        best_end_idx = 1
        for i in range(1, len(lyrics_left) + 1):
            trial = " ".join(lyrics_left[:i])
            sim = jaccard_similarity(trial, segment["text"])
            if sim > best_sim:
                best_sim = sim
                best_end_idx = i

        matched_lines = lyrics_left[:best_end_idx]
        lyrics_left = lyrics_left[best_end_idx:]

        fragments.append({
            "begin": f"{segment['start']:.3f}",
            "end": f"{segment['end']:.3f}",
            "lines": matched_lines
        })

    with open(output_sync_map, 'w') as f:
        json.dump({"fragments": fragments}, f, indent=2)



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python whisperx_script.py <vocals.wav> <lyrics.txt> <output_sync.json>")
        sys.exit(1)

    audio_path = sys.argv[1]
    lyrics_path = sys.argv[2]
    output_sync_map = sys.argv[3]

    sincronizeaza_versuri_whisperx(audio_path, lyrics_path, output_sync_map)

    # codul a fost adaptat după https://github.com/rye761/pysync/blob/master/pysync/sync.py
