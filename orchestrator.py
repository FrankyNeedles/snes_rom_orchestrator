import json
import requests
from asset_generator import SNESAssetGenerator
from state_manager import StateManager

class Orchestrator:
    """
    The Boss: LLM routes to asset/code, injects PVSnesLib sprite code hints.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = "meta-llama/llama-3.1-70b-instruct:free"
        self.state = StateManager()
        self.artist = SNESAssetGenerator()
        self.generated_code = None

    def ask_llm(self, prompt):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=120)
        return resp.json()['choices'][0]['message']['content'] if resp.status_code == 200 else None

    def execute_plan(self, user_prompt):
        system_prompt = """PVSnesLib C89 Expert. Output ONLY JSON {"action": "asset"|"code", "prompt": "desc", "details": "name or note"}.

Asset: pixel art sprite.
Code: C89 PVSnesLib code. For sprite "knight": knight_tiles (gfx), knight_palette (pal). Use sprInit(), sprSetVram(knight_tiles, knight_palette), sprSet().""" + self.state.get_context()
        full = system_prompt + "\nUser: " + user_prompt
        resp = self.ask_llm(full)
        print("[Boss] Response:", resp)
        try:
            task = json.loads(resp)
            if task["action"] == "asset":
                img = self.artist.generate_pixel_art(task["prompt"])
                if img:
                    meta = self.artist.crunch_to_snes(img, task["details"])
                    self.state.add_asset(meta)
            else:
                self.generated_code = task["details"]
        except:
            self.generated_code = """#include <snes.h>
#include <snes/snes.h>  // Sprites
extern const unsigned char knight_tiles[], knight_palette[];
int main(void) {
  consoleInit();
  sprInit();
  sprSetVram(knight_tiles, knight_palette);
  while (1) {
    sprSet();
    WaitForVBlank();
  }
  return 0;
}"""

    def get_skeleton(self):
        return self.generated_code or """#include <snes.h>
int main(void) {
  consoleInit();
  while(1) WaitForVBlank();
  return 0;
}"""

