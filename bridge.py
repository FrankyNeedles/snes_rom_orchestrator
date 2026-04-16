import os
import json
import subprocess
import re
from dotenv import load_dotenv
import requests
from pathlib import Path

load_dotenv('.env')

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
MODEL = os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3.5-sonnet')

def scan_assets():
    """Scan data/ for sprites/audio, gen assets.h consts."""
    sprites = list(Path('data/sprites').glob('*.[bp]mp')) + list(Path('data/sprites').glob('*.png'))
    audio = list(Path('data/audio').glob('*.wav')) + list(Path('data/audio').glob('*.{it,mod}'))
    
    consts = []
    for sprite in sprites:
        idx = len(consts)
        consts.append(f'#define SPR_{sprite.stem.upper()} {idx}')
    for sound in audio:
        idx = len(consts)
        consts.append(f'#define SFX_{sound.stem.upper()} {idx}')
    
    with open('assets.h', 'w') as f:
        f.write('// Auto-generated assets\n')
        f.write('\n'.join(consts))
    return consts

def prompt_to_blueprint(prompt, mode, audio):
    """Send to OpenRouter: NL → JSON blueprint."""
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': MODEL,
        'messages': [{
            'role': 'user',
            'content': f'''Translate to SNES JSON blueprint (mode: {mode}, audio: {audio}).

Prompt: {prompt}

Output ONLY JSON: {{
  "mode": "{mode}",
  "audio": "{audio}",
  "actors": [{{...}}],
  "timeline": [{{ "frame": N, "action": "move", "actor": 0, "x": 50, "y": 30 }}],
  "custom_c": "// Insert C code here (math, regs)",
  "init": "// Actor init"
}}'''
        }]
    }
    resp = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=data)
    blueprint_str = resp.json()['choices'][0]['message']['content']
    blueprint = json.loads(blueprint_str)
    return blueprint

def generate_c_from_template(blueprint):
    """Fill mega_engine.c template → main.c."""
    with open('mega_engine.c', 'r') as f:
        template = f.read()
    
    timeline_str = ''
    for event in blueprint.get('timeline', []):
        timeline_str += f'    timeline[{len(timeline_str)//50}].frame = {event.get("frame",0)};\n'
        # etc. parse actions
    
    custom = blueprint.get('custom_c', '// No custom')
    
    main_c = template.replace('// INSERT_TIMELINE_EVENTS_HERE', timeline_str)
    main_c = main_c.replace('// INSERT_CUSTOM_LOGIC_HERE', custom)
    # Add more replacements
    
    with open('main.c', 'w') as f:
        f.write(main_c)

def compile_rom():
    """Sixpack assets, make, launch if success."""
    # Assume sixpack from SNES-IDE
    subprocess.run(['../SNES-IDE/resources/bin/windows/sixpack/sixpack', '-vlif', 'data/', 'build/data/'], check=True)
    result = subprocess.run(['make'], cwd='.', capture_output=True, text=True)
    if result.returncode == 0:
        return 'build/game.sfc'
    else:
        raise Exception(f'Compile failed: {result.stderr}')

def generate_rom(prompt, mode, audio):
    """Full pipeline."""
    scan_assets()
    blueprint = prompt_to_blueprint(prompt, mode, audio)
    generate_c_from_template(blueprint)
    rom_path = compile_rom()
    return rom_path
