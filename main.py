import sys
from orchestrator import SNESOrchestrator
from foundry import SNESFoundry

def main():
    # 1. Setup your credentials (Replace with your actual OpenRouter key)
    # Strategy: Using OpenRouter's free/cheap tier
    OPENROUTER_API_KEY = "OPENROUTER_API" # <-- Replace with your OpenRouter API key
    
    if OPENROUTER_API_KEY == "OPENROUTER_API":
        print("[!] Warning: No API Key found. Please add your OpenRouter key to main.py")
        # return

    # 2. Wake up the team
    boss = SNESOrchestrator(api_key="OPENROUTER_API")
    body = SNESFoundry()
    
    print("=== SNES ROM ORCHESTRATOR ONLINE ===")
    print("Senior Team: Architect (Claude), Artist (Flux), Coder (Nemotron) are ready.")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\n[You]: ")
        
        if user_input.lower() in ["quit", "exit"]:
            break

        # Step 1: Orchestrate the request
        # The Boss decides if we need an Image (Artist) or Code (Foundry)
        print("[Boss] Processing your request...")
        boss.execute_plan(user_input)

        # Step 2: The "Silent Fixer" (Auto-Surgery Loop)
        # If the Boss generated code, we try to 'Bake' it.
        # We give the AI 3 'Lives' to fix its own mistakes.
        attempts = 0
        success = False
        
        while attempts < 3 and not success:
            # Note: This is a simplified logic flow. 
            # In your full system, the Orchestrator would store the latest code.
            
            # For this example, let's assume the AI generated 'main.c'
            # We call the Foundry to try and compile it.
            # print(f"[Foundry] Bake attempt {attempts + 1}...")
            # result = body.bake_rom("... code from orchestrator ...")
            
            # if result["status"] == "success":
            #     print("[System] BAKE SUCCESSFUL! Your ROM is ready.")
            #     success = True
            # else:
            #     print(f"[Immune System] Error found: {result['message']}")
            #     print("[Immune System] Sending error back to the AI for surgery...")
            #     # Feed the error back to the Boss to generate fixed code
            #     # fixed_code = boss.ask_the_brain(f"FIX THIS ERROR: {result['message']}")
            #     attempts += 1
            
            # For now, let's just break the loop until the full 
            # Foundry-Orchestrator variable passing is wired up.
            break

if __name__ == "__main__":
    main()