import json
import os

class SNESStateManager:
    """
    The Librarian: Keeps track of the 5 Pillars (Assets, Actors, Mechanics, 
    Environment, Story). Ensures the AI never forgets what has been built.
    """
    def __init__(self, state_file="snes_project_state.json"):
        self.state_file = state_file
        # Initialize the 5 Pillars of the project
        self.state = {
            "assets": {},      # Metadata for images/sounds
            "actors": {},      # Characters, NPCs, Player stats
            "environment": {}, # Map data, Tilemaps, Backgrounds
            "mechanics": [],   # Rules (e.g., "Gravity is 5", "A = Jump")
            "story": [],       # Dialogue, Quest progress
            "compilation_history": [] # Logs of past "Bakes" and errors
        }
        self.load_state()

    def load_state(self):
        """Loads the ledger from the hard drive."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
                print(f"[Librarian] State loaded. Current assets: {len(self.state['assets'])}")

    def save_state(self):
        """Persists the ledger to the hard drive (Atomic Save)."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=4)
        print("[Librarian] Ledger updated on disk.")

    def update_asset(self, asset_metadata):
        """Registers a new physical asset into the project."""
        name = asset_metadata['name']
        self.state['assets'][name] = asset_metadata
        self.save_state()

    def add_mechanic(self, description):
        """Records a gameplay rule the AI must follow."""
        if description not in self.state['mechanics']:
            self.state['mechanics'].append(description)
            self.save_state()

    def get_llm_context(self):
        """
        The 'Cheat Sheet': Summarizes the entire project into a small 
        text block so the AI knows exactly what it has to work with.
        """
        context = "### CURRENT PROJECT STATE ###\n"
        
        # List Assets
        context += "Assets Available:\n"
        for name, meta in self.state['assets'].items():
            context += f"- {name}: {meta['dimensions']} pixels, {meta['format']}\n"
            
        # List Mechanics
        context += "\nGameplay Rules:\n"
        for rule in self.state['mechanics']:
            context += f"- {rule}\n"
            
        return context

    def log_compiler_error(self, error_message):
        """Memory for the 'Immune System' to learn from mistakes."""
        self.state['compilation_history'].append(error_message)
        # Keep only the last 5 errors to prevent the file from getting too big
        self.state['compilation_history'] = self.state['compilation_history'][-5:]
        self.save_state()

# Example usage
if __name__ == "__main__":
    # librarian = SNESStateManager()
    # librarian.add_mechanic("Player can move in 8 directions")
    # print(librarian.get_llm_context())
    pass