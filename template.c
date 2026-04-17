#include <snes.h>

// [[ASSETS]] - The AI will put image declarations here

int main(void) {
    // Initialize SNES hardware
    consoleInit();

    // [[INITIALIZATION]] - The AI will setup sprites and backgrounds here

    // Wait for VGA sync
    setScreenOn();

    while (1) {
        // [[GAME_LOOP]] - The AI will handle movement and input here

        // Wait for next frame
        setBrightness(0); // Basic flicker prevention
        WaitForVBlank();
    }
    return 0;
}