import subprocess
import os

class SNESFoundry:
    """
    The Body: Physically compiles the code into a ROM.
    Uses a 'Skeleton' strategy to keep budget AI models on track.
    """
    def __init__(self, tools_path="devkitsnes/bin", project_dir="."):


        self.tools_path = tools_path
        self.project_dir = project_dir
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))


    def get_skeleton_template(self):
        """
        The Gold-Standard: This code is 100% guaranteed to compile.
        The AI is only allowed to inject logic into 'USER_LOGIC_HERE'.
        """
        return """
#include <snes.h>

// Pre-defined palette and graphics pointers
extern byte patterns, patterns_end;
extern byte palette;

int main(void) {
    // 1. Initialize the SNES hardware
    consoleInit();

    // 2. Load the assets (This is where the Librarian helps)
    // [ASSET_LOADING_HERE]

    // 3. Set the screen to the correct mode
    setMode(BG_MODE1, 0);
    bgSetDisable(1);
    bgSetDisable(2);
    setScreenOn();

    while (1) {
        // [USER_LOGIC_HERE]
        
        // Wait for the 'Heartbeat' of the SNES (V-Blank)
        WaitForVBlank();
    }
    return 0;
}
"""

    def bake_rom(self, c_code):
        """
        The Surgery: Takes the AI's code, saves it, and runs the compiler.
        """
        source_path = os.path.join(self.BASE_DIR, "main.c")

        with open(source_path, "w") as f:
            f.write(c_code)

        self.preprocess_assets()
        print("[Foundry] Starting the Bake... (Calling 816-tcc)")
        
        # This command simulates running your compiler. 
        # You will need to adjust the command to match your specific .bat or .sh file.
        try:
            # Running the compiler and capturing 'The Screams' (stderr)
            make_exe = os.path.join(self.BASE_DIR, self.tools_path, "make.exe")
            result = subprocess.run(
                [make_exe], shell=True,
                cwd=self.BASE_DIR,
                capture_output=True,
                text=True,
                timeout=30
            )



            if result.return_code == 0:
                print("[Success] ROM Baked Successfully: game.sfc")
                return {"status": "success", "file": "game.sfc"}

            else:
                print("[Foundry] Compiler Screamed! Capturing errors...")
                return {"status": "error", "message": result.stderr}

        except Exception as e:
            return {"status": "crash", "message": str(e)}

    def preprocess_assets(self):
        """Convert BMP assets to SNES format with gfx2snes."""
        import glob
        gfx_exe = os.path.join(self.BASE_DIR, "devkitsnes", "tools", "gfx2snes.exe")
        assets_dir = os.path.join(self.BASE_DIR, "assets")
        data_dir = os.path.join(self.BASE_DIR, "data")
        os.makedirs(data_dir, exist_ok=True)
        if os.path.exists(gfx_exe):
            for bmp in glob.glob(os.path.join(assets_dir, "*.bmp")):
                name = os.path.splitext(os.path.basename(bmp))[0]
                try:
                    result = subprocess.run([gfx_exe, bmp], cwd=data_dir, capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        print(f"[Asset] Converted {name}.bmp")
                    else:
                        print(f"[Asset] gfx2snes error for {name}: {result.stderr}")
                except Exception as e:
                    print(f"[Asset] Exception for {name}: {e}")
        else:
            print("[Asset] gfx2snes.exe not found")

    def generate_build_script(self):
        """Ensures the hdr.asm and Makefile are correctly placed."""
        # This part ensures the 'Ancient Syntax' files are fixed and hard-coded
        pass

