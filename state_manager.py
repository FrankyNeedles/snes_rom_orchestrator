import json
import os

class ProjectManager:
    def __init__(self, filename="project_state.json"):
        self.filename = filename
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            self.reset_state()
        
        os.makedirs("assets/raw", exist_ok=True)
        os.makedirs("assets/compiled", exist_ok=True)
        
    def reset_state(self):
        default_state = {
            "project_info": {"name": "New Game", "version": "0.1"},
            "pillars": {
                "actors": [],
                "environment": {},
                "mechanics": [],
                "assets": [],
                "story_dialogue": []
            },
            "history": [] 
        }
        self.save_state(default_state)

    def load_state(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except:
            self.reset_state()
            return self.load_state()

    def save_state(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def update_pillar(self, pillar_name, new_data):
        state = self.load_state()
        if pillar_name in state["pillars"]:
            if isinstance(state["pillars"][pillar_name], list):
                # Only add if it's not already there
                for item in new_data:
                    if item not in state["pillars"][pillar_name]:
                        state["pillars"][pillar_name].append(item)
            else:
                state["pillars"][pillar_name] = new_data
            self.save_state(state)

    def add_lesson(self, lesson_text):
        state = self.load_state()
        state["history"].append(lesson_text)
        self.save_state(state)