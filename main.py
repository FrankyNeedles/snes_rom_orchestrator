import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
  print("Set OPENROUTER_API_KEY in .env")
  exit(1)

from orchestrator import Orchestrator
from foundry import SNESFoundry

boss = Orchestrator(OPENROUTER_API_KEY)
body = SNESFoundry()

print("=== SNES ROM ORCHESTRATOR ===")
print("Artist (Pollinations), Brain (Llama3.1), Body (816-tcc)")
print("Type 'quit' to exit.")

while True:
  user_input = input("\n[You]: ")
  if user_input.lower() in ["quit", "exit"]:
    break

  boss.execute_plan(user_input)

  code = getattr(boss, 'generated_code', None)
  if not code:
    code = boss.get_skeleton()

  success = False
  for attempt in range(3):
    print(f"[Silent Fixer] Attempt {attempt+1}/3")
    result = body.bake_rom(code)
    if result["status"] == "success":
      print("🎮 ROM ready: snes_rom_orchestrator/game.sfc")
      success = True
      break
    else:
      error = result["stderr"]
      print("[Error]", error[:200] + "..." if len(error) > 200 else error)
      fix_prompt = f"Fix this C89 PVSnesLib error: {error}\nCurrent code:\\n{code}\\nOutput ONLY the fixed code."
      code = boss.ask_llm(fix_prompt)
      if not code:
        break

  if not success:
    print("Failed after 3 attempts. Check Makefile/PVSnesLib paths.")

