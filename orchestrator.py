import os
import json
import requests
from asset_generator import SNESAssetGenerator
from state_manager import ProjectManager


class SNESOrchestrator:
    """
    The Boss: Coordinates the AI Brain, the Artist, and the Librarian.
    It takes your high-level ideas and turns them into technical tasks.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = "anthropic/claude-3.5-sonnet" # The 'Smart' brain for logic
        self.librarian = ProjectManager("project_state.json")

        self.artist = SNESAssetGenerator(api_key=api_key)
        
    def ask_the_brain(self, user_prompt):
        """Sends the project state + your request to the AI Brain."""
        
        # 1. Get the current 'Source of Truth' from the Librarian
        current_context = self.librarian.get_llm_context()
        
        # 2. Build the 'System Prompt' (The Rules of the Game)
        system_instruction = (
            "You are the Lead SNES Developer. You follow C89 standards. "
            "You never use modern C features like mid-block variable declarations. "
            "Your goal is to output tasks in JSON format: {'action': 'generate_asset'|'write_code', 'details': '...'}"
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 3. Combine everything into one request
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Project State:\n{current_context}\n\nUser Request: {user_prompt}"}
            ]
        }

        print("[Brain] Thinking...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        return response.json()['choices'][0]['message']['content']

    def execute_plan(self, user_input):
        """The main loop: User says 'Make a forest', Boss makes it happen."""
        
        # Step 1: Ask the Brain what to do
        brain_response = self.ask_the_brain(user_input)
        print(f"[Brain] Decision: {brain_response}")

        # Note: In a production version, we would parse JSON here.
        # For now, let's look for keywords to trigger our sub-systems.
        
        if "generate_asset" in brain_response.lower() or "create" in user_input.lower():
            # Example: User said 'Create a knight'
            asset_name = user_input.split()[-1] # Simple logic to get the name
            
            # Step 2: Tell the Artist to draw
            raw_img = self.artist.generate_pixel_art(user_input)
            if raw_img:
                path = self.artist.crunch_to_snes(raw_img, asset_name)
                
                # Step 3: Tell the Librarian to record it
                meta = self.artist.get_asset_metadata(asset_name, path)
                self.librarian.update_asset(meta)
                print(f"[Boss] Asset {asset_name} is now in the ledger.")

        if "code" in brain_response.lower() or "logic" in brain_response.lower():
            print("[Boss] Logic generation triggered. (Next file: The Foundry)")

# Testing logic
if __name__ == "__main__":
    # key = "your_openrouter_key"
    # boss = SNESOrchestrator(api_key=key)
    # boss.execute_plan("Create a pixel art green forest background")
    pass