# video_generator.py
import sys
import json
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ColorClip
from moviepy.config import change_settings as mpy_config

mpy_config({'IMAGEMAGICK_BINARY': '/opt/homebrew/bin/convert'})

def creeaza_video(original_audio_path, sync_map_path, output_video_path):
    with open(sync_map_path, 'r') as f:
        sync_data = json.load(f)

    audio = AudioFileClip(original_audio_path)
    duration = audio.duration
    clips = []

    fragments = sync_data.get("fragments", [])
    if fragments:
        first_start = float(fragments[0]["begin"])
        if first_start > 0:
            clips.append(ColorClip(size=(1280, 720), color=(0, 0, 0), duration=first_start).set_start(0))

        for fragment in fragments:
            start = float(fragment["begin"])
            end = float(fragment["end"])
            text = "\n".join(fragment["lines"])

            txt_clip = TextClip(
                text,
                fontsize=50,
                color='white',
                size=(1280, 720),
                method='caption',
                align='center'
            ).set_position('center').set_start(start).set_duration(end - start)

            clips.append(txt_clip)

    background = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=duration)
    final = CompositeVideoClip([background] + clips)
    final = final.set_audio(audio)
    final.write_videofile(output_video_path, fps=24, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python video_generator.py <audio_path> <sync_json> <output_video>")
        sys.exit(1)

    audio_path = sys.argv[1]
    sync_json = sys.argv[2]
    output_video = sys.argv[3]

    creeaza_video(audio_path, sync_json, output_video)