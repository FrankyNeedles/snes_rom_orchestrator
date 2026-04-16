import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
from dotenv import load_dotenv
from bridge import generate_rom  # Bridge logic

load_dotenv('.env')

class SNESOrchestratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate SNES ROM Orchestrator")
        self.root.geometry("800x600")

        # Mode toggle
        tk.Label(root, text="Mode:").pack(pady=5)
        self.mode_var = tk.StringVar(value="video")
        mode_frame = ttk.Frame(root)
        mode_frame.pack()
        tk.Radiobutton(mode_frame, text="Animated Video", variable=self.mode_var, value="video").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Interactive Game", variable=self.mode_var, value="game").pack(side=tk.LEFT)

        # Audio toggle
        tk.Label(root, text="Audio:").pack(pady=5)
        self.audio_var = tk.StringVar(value="bgm")
        audio_frame = ttk.Frame(root)
        audio_frame.pack()
        tk.Radiobutton(audio_frame, text="Background Music", variable=self.audio_var, value="bgm").pack(side=tk.LEFT)
        tk.Radiobutton(audio_frame, text="Sound Effects", variable=self.audio_var, value="sfx").pack(side=tk.LEFT)

        # Prompt input
        tk.Label(root, text="Natural Language Prompt:").pack(pady=5)
        self.prompt_text = scrolledtext.ScrolledText(root, height=15, width=90, wrap=tk.WORD)
        self.prompt_text.pack(pady=5)

        # Generate button
        ttk.Button(root, text="GENERATE ROM", command=self.on_generate).pack(pady=10)

        ttk.Button(root, text="Clear", command=self.clear_prompt).pack()

    def on_generate(self):
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        mode = self.mode_var.get()
        audio = self.audio_var.get()
        if not prompt:
            messagebox.showwarning("Warning", "Enter a prompt!")
            return
        try:
            rom_path = generate_rom(prompt, mode, audio)
            messagebox.showinfo("Success", f"ROM generated: {rom_path}\nLaunching emulator...")
            os.system(f"../SNES-IDE/resources/bin/windows/bsnes/bsnes.exe {rom_path}")  # Adjust path/OS
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_prompt(self):
        self.prompt_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SNESOrchestratorGUI(root)
    root.mainloop()
