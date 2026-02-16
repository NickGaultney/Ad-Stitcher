import os
from moviepy import *

hooks_dir = "Hook"
meat_dir = "Meat"
cta_dir = "CTA"
output_dir = "Final"

os.makedirs(output_dir, exist_ok=True)

# Get all mp4 files
hook_files = [f for f in os.listdir(hooks_dir) if f.endswith(".mp4")]
meat_files = [f for f in os.listdir(meat_dir) if f.endswith(".mp4")]
cta_files = [f for f in os.listdir(cta_dir) if f.endswith(".mp4")]

for hook_name in hook_files:
    for meat_name in meat_files:
        for cta_name in cta_files:

            hook_path = os.path.join(hooks_dir, hook_name)
            meat_path = os.path.join(meat_dir, meat_name)
            cta_path = os.path.join(cta_dir, cta_name)

            print(f"Combining {hook_name} + {meat_name} + {cta_name}")

            hook_clip = VideoFileClip(hook_path)
            meat_clip = VideoFileClip(meat_path)
            cta_clip = VideoFileClip(cta_path)

            final = concatenate_videoclips([hook_clip, meat_clip, cta_clip])

            output_name = f"{os.path.splitext(hook_name)[0]}_{os.path.splitext(meat_name)[0]}_{os.path.splitext(cta_name)[0]}.mp4"
            output_path = os.path.join(output_dir, output_name)

            final.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac"
            )

            hook_clip.close()
            meat_clip.close()
            cta_clip.close()
            final.close()

print("Done 🎬")
