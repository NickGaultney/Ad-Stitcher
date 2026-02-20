import os, gc
from moviepy import *
from moviepy.audio.fx import all as afx

hooks_dir = "Hook"
meat_dir = "Meat"
cta_dir = "CTA"
output_dir = "Final"
cache_dir = "Cache_HookMeat"
music_path = "music.mp3"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(cache_dir, exist_ok=True)

hook_files = [f for f in os.listdir(hooks_dir) if f.endswith(".mp4")]
meat_files = [f for f in os.listdir(meat_dir) if f.endswith(".mp4")]
cta_files  = [f for f in os.listdir(cta_dir)  if f.endswith(".mp4")]

# Load music ONCE (avoid re-decoding 900 times)
bg_master = AudioFileClip(music_path).volumex(0.3)

try:
    # 1) Build/cache Hook+Meat intermediates (300 total)
    for hook_name in hook_files:
        for meat_name in meat_files:
            hook_path = os.path.join(hooks_dir, hook_name)
            meat_path = os.path.join(meat_dir, meat_name)

            hm_name = f"{os.path.splitext(hook_name)[0]}_{os.path.splitext(meat_name)[0]}.mp4"
            hm_path = os.path.join(cache_dir, lca)

            if not os.path.exists(hm_path):
                with VideoFileClip(hook_path) as hook_clip, VideoFileClip(meat_path) as meat_clip:
                    hm = concatenate_videoclips([hook_clip, meat_clip], method="chain")
                    hm.write_videofile(
                        hm_path,
                        codec="libx264",
                        audio_codec="aac",
                    )
                    hm.close()
                    gc.collect()

    # 2) Append CTA + add background music (900 total)
    for hm_file in [f for f in os.listdir(cache_dir) if f.endswith(".mp4")]:
        hm_path = os.path.join(cache_dir, hm_file)

        for cta_name in cta_files:
            cta_path = os.path.join(cta_dir, cta_name)

            out_name = f"{os.path.splitext(hm_file)[0]}_{os.path.splitext(cta_name)[0]}.mp4"
            out_path = os.path.join(output_dir, out_name)

            if os.path.exists(out_path):
                continue

            with VideoFileClip(hm_path) as hm_clip, VideoFileClip(cta_path) as cta_clip:
                final = concatenate_videoclips([hm_clip, cta_clip], method="chain")

                # loop/trim music without reloading file
                bg = bg_master
                if bg.duration < final.duration:
                    bg = afx.audio_loop(bg, duration=final.duration)
                else:
                    bg = bg.subclip(0, final.duration)

                if final.audio:
                    combined = CompositeAudioClip([final.audio, bg])
                else:
                    combined = bg

                final = final.set_audio(combined)

                final.write_videofile(
                    out_path,
                    codec="libx264",
                    audio_codec="aac",
                )

                # critical cleanup (prevents “leaks” / file handle buildup)
                combined.close()
                final.close()
                gc.collect()

finally:
    bg_master.close()

print("Done 🎬")