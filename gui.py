import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import json
import os
import subprocess
import re
from dotenv import load_dotenv

# Import our Librarian
from state_manager import ProjectManager

# --- AI CONNECTIVITY ---
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

class SNESOrchestratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SNES ROM Orchestrator - Phase 4 (Titanium)")
        self.root.geometry("1100x850")
        self.root.configure(bg="#2c3e50")

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.manager = ProjectManager(os.path.join(self.BASE_DIR, "project_state.json"))
        self.chat_history = []
        
        self.llm = ChatOpenAI(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.1, 
            timeout=180
        )

        self.BIN_DIR = os.path.join(self.BASE_DIR, "devkitsnes", "bin")
        self.MAKE_PATH = os.path.join(self.BIN_DIR, "make.exe")

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_panel = tk.Frame(self.main_frame, bg="#2c3e50")
        self.left_panel.pack(side="left", fill="both", expand=True)
        self.chat_display = scrolledtext.ScrolledText(self.left_panel, state='disabled', wrap='word', bg="#ecf0f1", font=("Segoe UI", 10))
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)
        self.user_input = tk.Entry(self.left_panel, font=("Arial", 12))
        self.user_input.pack(fill="x", padx=5, pady=10)
        self.user_input.bind("<Return>", lambda e: self.send_message())

        self.right_panel = tk.Frame(self.main_frame, bg="#34495e", width=400)
        self.right_panel.pack(side="right", fill="both", padx=5)
        
        tk.Label(self.right_panel, text="Shadow Structure", bg="#34495e", fg="white").pack()
        self.state_display = scrolledtext.ScrolledText(self.right_panel, height=18, state='disabled', bg="#1a252f", fg="#2ecc71")
        self.state_display.pack(fill="x", padx=10)

        tk.Label(self.right_panel, text="Foundry Status", bg="#34495e", fg="white").pack()
        self.foundry_log = scrolledtext.ScrolledText(self.right_panel, height=12, state='disabled', bg="#1a252f", fg="#e67e22")
        self.foundry_log.pack(fill="x", padx=10)

        self.bake_btn = tk.Button(self.right_panel, text="🔥 GENERATE ROM", command=self.start_bake_thread, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), height=2)
        self.bake_btn.pack(fill="x", side="bottom", padx=20, pady=20)

        self.update_displays()

    def log_foundry(self, message):
        self.foundry_log.config(state='normal')
        self.foundry_log.insert(tk.END, f"> {message}\n")
        self.foundry_log.config(state='disabled')
        self.foundry_log.see(tk.END)

    def start_bake_thread(self):
        self.bake_btn.config(state='disabled', text="BAKING...")
        threading.Thread(target=self.foundry_process, daemon=True).start()

    def foundry_process(self):
        state = self.manager.load_state()
        attempts = 0
        success = False
        
        code = self.generate_initial_code(state)
        if not code:
            self.log_foundry("Error: AI Timeout.")
            self.root.after(0, self.reset_bake_button)
            return

        while attempts < 3 and not success:
            attempts += 1
            self.log_foundry(f"Bake Attempt {attempts}/3...")
            
            with open(os.path.join(self.BASE_DIR, "main.c"), "w") as f:
                f.write(code)

            try:
                cmd = f'"{self.MAKE_PATH}"'
                result = subprocess.run(cmd, capture_output=True, text=True, shell=True, cwd=self.BASE_DIR)
                
                if result.returncode == 0:
                    self.log_foundry("SUCCESS! game.sfc generated.")
                    success = True
                    messagebox.showinfo("Success", "ROM Created!")
                else:
                    self.log_foundry("Build Error. Fixing...")
                    print(f"--- COMPILER ERROR ---\n{result.stderr}\n-------------------")
                    code = self.ask_ai_to_fix(code, result.stderr)
                    if not code: break
            except Exception as e:
                self.log_foundry(f"Foundry Crash: {str(e)}")
                break

        self.root.after(0, self.update_displays)
        self.root.after(0, self.reset_bake_button)

    def generate_initial_code(self, state):
        self.log_foundry("Synthesizing Strict C Code...")
        
        # We provide a PERFECT SKELETON for the AI to fill
        skeleton = """
        #include <snes.h>
        
        int main(void) {
            // [VARS] Declare variables here (C89 style)
            
            consoleInit();
            
            // [LOGIC] Add game logic here
            
            while(1) {
                // [LOOP] Add game loop here
                WaitForVBlank();
            }
            return 0;
        }
        """

        prompt = f"""
        Act as a Professional PVSnesLib Developer.
        Fill this skeleton based on the Pillars: {json.dumps(state['pillars'])}
        
        SKELETON:
        {skeleton}
        
        RULES:
        - NEVER use subfolders in includes (Use #include <snes.h> ONLY).
        - End every C line with a semicolon (;).
        - Return ONLY the full main.c code. No chatter.
        """
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)]).content
            return response.strip().replace("```c", "").replace("```", "")
        except: return None

    def ask_ai_to_fix(self, broken_code, error_log):
        self.log_foundry("Silent Fixer is repairing...")
        prompt = f"FIX THIS SNES C CODE.\nERROR: {error_log}\nCODE: {broken_code}\nReturn ONLY fixed code. No backticks."
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)]).content
            return response.strip().replace("```c", "").replace("```", "")
        except: return None

    def reset_bake_button(self):
        self.bake_btn.config(state='normal', text="🔥 GENERATE ROM")

    def update_displays(self):
        state = self.manager.load_state()
        self.state_display.config(state='normal')
        self.state_display.delete(1.0, tk.END)
        self.state_display.insert(tk.END, json.dumps(state["pillars"], indent=2))
        self.state_display.config(state='disabled')

    def log_to_chat(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def send_message(self):
        query = self.user_input.get()
        if not query: return
        self.log_to_chat("You", query)
        self.user_input.delete(0, tk.END)
        threading.Thread(target=self.ai_architect_logic, args=(query,), daemon=True).start()

    def ai_architect_logic(self, user_query):
        state = self.manager.load_state()
        system_msg = SystemMessage(content=f"You are the SNES Architect. State: {json.dumps(state['pillars'])}. Use [UPDATE_STATE] {{json}} for changes.")
        messages = [system_msg] + self.chat_history[-5:] + [HumanMessage(content=user_query)]

        try:
            response = self.llm.invoke(messages).content
            state_match = re.search(r"\[UPDATE_STATE\]\s*(\{.*?\})", response, re.DOTALL)
            clean_chat = re.sub(r"\[UPDATE_STATE\].*?$", "", response, flags=re.DOTALL)
            self.log_to_chat("Architect", clean_chat.strip())
            self.chat_history.append(HumanMessage(content=user_query))
            self.chat_history.append(AIMessage(content=clean_chat))
            if state_match:
                new_data = json.loads(state_match.group(1))
                for p, d in new_data.items(): self.manager.update_pillar(p, d)
            self.root.after(0, self.update_displays)
        except Exception as e:
            self.log_to_chat("System", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SNESOrchestratorGUI(root)
    root.mainloop()