# pvsneslib standard Makefile template
# Assumes toolchain from ../SNES-IDE/resources/bin/windows/ or set PATH

CC = wla-65816
CFLAGS = -I ../SNES-IDE/resources/libs/pvsneslib/include -opt
AS = ca65
AFLAGS = -t 65816 -I ../SNES-IDE/resources/libs/pvsneslib/include
LD = ld65

TARGET = build/game.sfc
ROMNAME = GAME

all: $(TARGET)

$(TARGET): main.o data.o
	$(LD) -C ../SNES-IDE/resources/libs/pvsneslib/config/lorom_32k_vertical.cfg -o $(TARGET) main.o data.o pvsneslib.lib

main.o: mega_engine.c
	$(CC) $(CFLAGS) -c mega_engine.c -o main.o

data.o: data.asm
	$(AS) $(AFLAGS) data.asm -o data.o

sixpack: data/
	../SNES-IDE/resources/bin/windows/sixpack/sixpack -vlif data/ build/data/

clean:
	rm -f *.o $(TARGET)

run: $(TARGET)
	../SNES-IDE/resources/bin/windows/bsnes/bsnes.exe $(TARGET)

# Adjust paths for your OS (windows/linux/macos bins in SNES-IDE/resources/bin/)

