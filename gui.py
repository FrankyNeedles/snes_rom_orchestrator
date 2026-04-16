import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from phase3_langchain_bridge import Phase3Bridge

class SNESOrchestratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate SNES ROM Orchestrator")
        self.root.geometry("600x450")
        
        # Build the AI machine once
        self.bridge = Phase3Bridge()

        # UI Layout
        tk.Label(root, text="Describe your SNES Scene:", font=("Arial", 12, "bold")).pack(pady=10)
        self.prompt_entry = tk.Text(root, height=5, width=60, font=("Consolas", 10))
        self.prompt_entry.pack(pady=5)

        self.mode_var = tk.StringVar(value="video")
        tk.Radiobutton(root, text="Animated Scene", variable=self.mode_var, value="video").pack()
        tk.Radiobutton(root, text="Interactive Game", variable=self.mode_var, value="game").pack()

        self.btn_generate = tk.Button(root, text="GENERATE & RUN ROM", command=self.run_pipeline, 
                                     bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), height=2, width=25)
        self.btn_generate.pack(pady=20)

        self.status_label = tk.Label(root, text="Status: Ready", fg="#34495e")
        self.status_label.pack()

    def run_pipeline(self):
        prompt = self.prompt_entry.get("1.0", "end-1c")
        mode = self.mode_var.get()
        
        if not prompt.strip():
            messagebox.showwarning("Empty Prompt", "Please tell the AI what to build!")
            return

        try:
            self.status_label.config(text="Status: AI is coding...", fg="orange")
            self.root.update()

            # 1. AI Generates the C code
            c_code = self.bridge.generate_blueprint(prompt, mode, "None")

            # 2. Write code to file
            self.bridge.write_to_engine(c_code)

            # 3. Compile the ROM
            self.status_label.config(text="Status: Baking ROM (Running Make)...", fg="blue")
            self.root.update()
            
            # Note: We run make from inside the snes_rom_orchestrator folder
            make_path = os.path.join("devkitsnes", "bin", "make.exe")
            result = subprocess.run([make_path], capture_output=True, text=True)

            if result.returncode == 0:
                self.status_label.config(text="Status: SUCCESS!", fg="green")
                # 4. Launch Emulator
                emu_path = os.path.join("emulators", "snes9x.exe")
                rom_path = os.path.join("build", "game.sfc")
                if os.path.exists(rom_path):
                    subprocess.Popen([emu_path, rom_path])
            else:
                # Show the exact line number where the AI messed up
                messagebox.showerror("Compiler Error", result.stderr)
                self.status_label.config(text="Status: Compiler Failed", fg="red")

        except Exception as e:
            messagebox.showerror("System Error", str(e))
            self.status_label.config(text="Status: System Crash", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = SNESOrchestratorGUI(root)
    root.mainloop()