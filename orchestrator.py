import json
import os
import requests
from asset_generator import SNESAssetGenerator
from state_manager import StateManager

class Orchestrator:
    """
    The Boss: Routes user requests to Artist or Coder via Llama3.1.
    Demands JSON.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = "meta-llama/llama-3.1-70b-instruct:free"
        self.state = StateManager()
        self.artist = SNESAssetGenerator()
        self.generated_code = None

    def ask_llm(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=120)
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content']
        return None

    def execute_plan(self, user_prompt):
        system_prompt = """You are SNES PVSnesLib expert. Output ONLY JSON.
Statements must be separated by newlines or semicolons.
{"action": "asset" or "code", "prompt": "detailed description", "details": "name or code comment"}
For asset: generate pixel art sprite.
For code: C89 code snippet for logic.
State: """ + self.state.get_context()
        full_prompt = system_prompt + "\nUser: " + user_prompt
        resp = self.ask_llm(full_prompt)
        print("[Boss] AI:", resp)
        try:
            task = json.loads(resp)
            action = task["action"]
            if action == "asset":
                img = self.artist.generate_pixel_art(task["prompt"])
                if img:
                    meta = self.artist.crunch_to_snes(img, task["details"])
                    self.state.add_asset(meta)
            elif action == "code":
                self.generated_code = task["details"]  # string code
        except:
            self.generated_code = self.get_skeleton()

    def get_skeleton(self):
        return """#include <snes.h>
int main(void) {
  consoleInit();
  while (1) {
    WaitForVBlank();
  }
  return 0;
}"""
