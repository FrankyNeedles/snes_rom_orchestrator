import requests
import os
from PIL import Image
from io import BytesIO

class SNESAssetGenerator:
    """
    Senior Artist: Free pixel art generation via Pollinations.ai + SNES crunching.
    """
    def __init__(self, output_dir="assets"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_pixel_art(self, prompt):
        print(f"[Artist] Dreaming: {prompt}")
        safe_prompt = prompt.replace(' ', '%20').replace(',', '%2C')
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=256&height=256&nologo=true&seed=42&model=FLUX.1-schnell"
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200:
            return Image.open(BytesIO(resp.content))
        print("[Artist] Generation failed")
        return None

    def crunch_to_snes(self, image, name, size=(32, 32)):
        print(f"[Cruncher] Processing '{name}' to SNES 16-color...")
        img = image.resize(size, Image.NEAREST)
        img = img.convert("P", palette=Image.ADAPTIVE, colors=16)
        path = os.path.join(self.output_dir, f"{name}.bmp")
        img.save(path)
        print(f"[Success] {path}")
        w, h = img.size
        return {
            "name": name,
            "path": path,
            "dimensions": f"{w}x{h}",
            "colors": 16
        }

if __name__ == "__main__":
    gen = SNESAssetGenerator()
    img = gen.generate_pixel_art("SNES pixel art red knight")
    if img:
        meta = gen.crunch_to_snes(img, "knight")
        print(meta)
