import subprocess
import os
import glob

class SNESFoundry:
    """
    The Body: Compiles C to SNES ROM using make.
    Converts assets/*.bmp with gfx2snes before build.
    """
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        pvsneslib_home = os.path.join(self.BASE_DIR, "pvsneslib")
        bin_path = os.path.join(pvsneslib_home, "bin")
        os.environ.setdefault("PVSNESLIB_HOME", pvsneslib_home)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = bin_path + os.pathsep + old_path
        print("[Foundry] PVSnesLib environment configured.")

    def bake_rom(self, c_code):
        main_path = os.path.join(self.BASE_DIR, "main.c")
        with open(main_path, "w") as f:
            f.write(c_code)

        # Graphics Pipeline: Convert all .bmp to SNES format
        assets_dir = os.path.join(self.BASE_DIR, "assets")
        gfx_exe = "gfx2snes.exe"  # Now in PATH
        print("[Foundry] Converting assets...")
        for bmp_file in glob.glob(os.path.join(assets_dir, "*.bmp")):
            name = os.path.splitext(os.path.basename(bmp_file))[0]
            cmd = f'{gfx_exe} -gb -pc16 -n "{bmp_file}"'
            result = subprocess.run(cmd, shell=True, cwd=self.BASE_DIR, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[Gfx] Converted {name}.bmp")
            else:
                print(f"[Gfx] Failed {name}: {result.stderr}")

        # Bake ROM
        print("[Foundry] Running make...")
        result = subprocess.run("make", shell=True, cwd=self.BASE_DIR, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("[Foundry] Success: game.sfc ready.")
            return {"status": "success", "file": "game.sfc"}
        else:
            print("[Foundry] Compiler error:", result.stderr[:300])
            return {"status": "error", "stderr": result.stderr}

