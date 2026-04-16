#include <snes.h>

int main(void) {
    // 1. Initialize the SNES console
    consoleInit();

    // 2. Set the background color to a nice Blue (Hex 0x4000)
    setbgcolor(RGB5(0,0,10));

    // 3. Wait for the SNES to "Refresh" (Infinite Loop)
    while(1) {
        WaitVBL();
    }
    return 0;
}