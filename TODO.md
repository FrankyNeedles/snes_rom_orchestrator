# SNES ROM Orchestrator TODO

## Progress Tracking

### Phase 1: Project Structure & Core Files [COMPLETE]
- [x] Create project directory structure
- [x] Create gui.py (Tkinter GUI with toggles, prompt input, generate button)
- [x] Create bridge.py (asset scan, JSON blueprint, code gen, compile logic)
- [x] Create mega_engine.c (pvsneslib template with frame-seq, timeline, audio, input)
- [x] Create Makefile (pvsneslib build)
- [x] Create data/sprites/ and data/audio/ dirs
- [x] Create build/ dir
- [x] Create .env template (for OpenRouter API key/model)
- [x] Create README.md

### Phase 2: Integration & Testing
- Integrate SNES-IDE toolchain (pvsneslib, sixpack, emulator)
- Test GUI → bridge flow
- Test compilation to .sfc
- Add sample assets

### Phase 3: AI Prompt Processing
- Implement OpenRouter API calls in bridge.py for NL → JSON blueprint
- Dynamic C code insertion (registers, paths, fades)

Updated after each step.

