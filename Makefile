# 1. SETUP PATHS
DEV_KIT_DIR := ./devkitsnes
LIB_DIR     := ./pvsneslib

# 2. TOOLS
CC      := $(DEV_KIT_DIR)/bin/816-tcc.exe
LD      := $(DEV_KIT_DIR)/bin/wlalink.exe

# 3. FOLDERS
INCLUDE := -I$(LIB_DIR)/include -I$(DEV_KIT_DIR)/include
TARGET  := build/game.sfc

# 4. THE RECIPE
all: $(TARGET)

$(TARGET): mega_engine.o
	@echo "Linking SNES ROM..."
	$(LD) -vr temp.link $(TARGET) $(LIB_DIR)/lib/pvsneslib.lib

mega_engine.o: mega_engine.c
	@echo "Compiling C code..."
	$(CC) $(INCLUDE) -c mega_engine.c -o mega_engine.o

clean:
	@echo "Cleaning old files..."
	-del /q *.o *.obj build\game.sfc 2>nul