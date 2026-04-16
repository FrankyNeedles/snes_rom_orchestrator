#include <snes.h>

void main() {
    consoleInit();

    // Set background color to purple-ish (RGB5: R=16, G=0, B=16)
    setColor(0, RGB5(16, 0, 16));

    while(1) {
        WaitVBL();
    }
}