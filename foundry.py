import subprocess
import os

class SNESFoundry:
    """
    The Body: Compiles C to SNES ROM using make.
    Captures errors for silent fixer.
    """
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        pvsneslib_home = os.path.join(self.BASE_DIR, "pvsneslib")
        bin_path = os.path.join(pvsneslib_home, "bin")
        os.environ.setdefault("PVSNESLIB_HOME", pvsneslib_home)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = bin_path + os.pathsep + old_path
        print("[Foundry] PVSnesLib env set")

    def bake_rom(self, c_code):
        main_path = os.path.join(self.BASE_DIR, "main.c")
        with open(main_path, "w") as f:
            f.write(c_code)
        print("[Foundry] Baking ROM...")
        result = subprocess.run("make", shell=True, cwd=self.BASE_DIR, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("[Foundry] Success: game.sfc")
            return {"status": "success", "file": "game.sfc"}
        else:
            print("[Foundry] Error:", result.stderr)
            return {"status": "error", "stderr": result.stderr}
