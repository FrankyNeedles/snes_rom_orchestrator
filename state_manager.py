import json
import os

class StateManager:
    def __init__(self, file="snes_project_state.json"):
        self.file = file
        self.state = {"Assets": [], "Logic": []}
        self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                self.state = json.load(f)

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.state, f, indent=4)

    def add_asset(self, meta):
        self.state["Assets"].append(meta)
        self.save()

    def add_logic(self, code):
        self.state["Logic"].append({"code": code})
        self.save()

    def get_context(self):
        assets = [a["name"] for a in self.state["Assets"]]
        logic = self.state["Logic"][-3:] if self.state["Logic"] else []
        return f"Assets: {assets}\nRecent Logic: {logic}"

if __name__ == "__main__":
    sm = StateManager()
    print(sm.get_context())

