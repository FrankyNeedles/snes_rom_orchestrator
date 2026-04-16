# Ultimate SNES ROM Orchestrator

Translates natural language to fully-featured SNES .sfc ROMs with animation, games, audio.

## Quick Start
```
cd snes_rom_orchestrator
pip install -r requirements.txt  # tkinter auto, requests for API
cp .env.example .env  # Set OPENROUTER_API_KEY, MODEL
python gui.py
```

Enter prompt like: "Make Mario walk in a circle with background music fading to black at frame 120"

Generate ROM → launches emulator.

## Structure
- `gui.py`: Tkinter interface
- `bridge.py`: Asset scan, AI prompt → JSON → C gen → compile
- `mega_engine.c`: pvsneslib template
- `data/`: sprites/audio assets
- `build/`: Generated ROMs

## Dev
Follow TODO.md. Leverages nearby SNES-IDE toolchain.

