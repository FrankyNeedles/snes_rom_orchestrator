import requests
import os
import json
from PIL import Image
from io import BytesIO

class SNESAssetGenerator:
    """
    The Senior Artist: Translates text prompts into SNES-compatible 
    16-color indexed bitmaps using OpenRouter and Image Processing.
    """
    def __init__(self, api_key, output_dir="assets"):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.output_dir = output_dir
        self.model = "black-forest-labs/flux.2-klein-4b" # Your budget choice
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_pixel_art(self, prompt):
        """Pass 1: Use OpenRouter to generate the 'Dream' image."""
        print(f"[Artist] Imagining: {prompt}...")
        
        # System instructions to force Pixel Art style
        full_prompt = (
            f"SNES 16-bit pixel art, {prompt}, flat colors, "
            "solid background, high contrast, crisp edges, "
            "Nintendo 1990s style."
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "prompt": full_prompt,
        }

        response = requests.post(
            f"{self.base_url}/images/generations",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            image_url = response.json()['data'][0]['url']
            return self._download_image(image_url)
        else:
            print(f"[Error] OpenRouter failed: {response.text}")
            return None

    def _download_image(self, url):
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    def crunch_to_snes(self, image, name, size=(32, 32)):
        """
        Pass 2: The 'Cruncher'. 
        Shrinks image to SNES resolution and reduces to 16 colors.
        """
        print(f"[Foundry] Crunching '{name}' to {size} pixels and 16 colors...")
        
        # 1. Resize to SNES scales (Nearest Neighbor keeps the pixels sharp)
        img = image.resize(size, Image.NEAREST)
        
        # 2. Quantize: Force the image into a 16-color palette
        # This is the 'Secret Sauce' that prevents SNES hardware crashes
        img = img.convert("P", palette=Image.ADAPTIVE, colors=16)
        
        # 3. Save as .bmp (pvsneslib/816-tcc prefers clean bitmaps)
        path = os.path.join(self.output_dir, f"{name}.bmp")
        img.save(path)
        
        print(f"[Success] Asset saved to: {path}")
        return path

    def get_asset_metadata(self, name, path):
        """Provides the 'Librarian' with the technical specs of the asset."""
        img = Image.open(path)
        width, height = img.size
        # We report tiles: SNES works in 8x8 blocks
        return {
            "name": name,
            "path": path,
            "dimensions": f"{width}x{height}",
            "tiles_wide": width // 8,
            "tiles_high": height // 8,
            "format": "4bpp" # 16 colors = 4 bits per pixel
        }

# Example usage for testing (if you run this file directly)
if __name__ == "__main__":
    # You would replace 'YOUR_KEY' with your actual OpenRouter key
    # generator = SNESAssetGenerator(api_key="sk-or-...")
    # raw_img = generator.generate_pixel_art("A green knight with a sword")
    # if raw_img:
    #     path = generator.crunch_to_snes(raw_img, "knight_sprite")
    #     print(generator.get_asset_metadata("knight_sprite", path))
    pass