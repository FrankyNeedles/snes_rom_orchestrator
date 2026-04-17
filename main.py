import os
import subprocess
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
  print("Add OPENROUTER_API_KEY to .env")
  exit(1)

from orchestrator import Orchestrator
from foundry import SNESFoundry

boss = Orchestrator(API_KEY)
body = SNESFoundry()

print("SNES Orchestrator - Ready!")
print("quit to exit.")

while True:
  user = input("\nYou: ")
  if user.lower() == 'quit': break
  boss.execute_plan(user)
  code = boss.get_skeleton()
  for att in range(3):
    print(f"Build {att+1}/3")
    res = body.bake_rom(code)
    if res['status'] == 'success':
      rom = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game.sfc")
      emu = r"C:\Users\frank\Projects\SNES_Studio\snes_rom_orchestrator\emulators\snes9x.exe"
      subprocess.Popen([emu, rom])
      print("ROM launched!")
      break
    code = boss.ask_llm(f"Fix C89 PVSnesLib error: {res['stderr']}\nCode:\n{code}\nFixed code ONLY.")

