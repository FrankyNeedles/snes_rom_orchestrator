# Run to copy sample assets from SNES-IDE examples
import shutil
import os

src_examples = '../SNES-IDE/docs/examples/'
dst_data = 'data/'

for ex in ['Pvsneslib.Example.hello_world/pvsneslibfont.png', 'Pvsneslib.Example.LikeMario/mariojump.wav', 'Pvsneslib.Example.LikeMario/mario_sprite.bmp']:
    src = os.path.join(src_examples, ex)
    if os.path.exists(src):
        dst = os.path.join(dst_data, os.path.basename(src))
        shutil.copy(src, dst)
        print(f"Copied {src} -> {dst}")

print("Sample assets ready!")
