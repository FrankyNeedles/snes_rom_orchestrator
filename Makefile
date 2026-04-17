# -------------------------------------------------------------------
# SNES ROM Orchestrator - Path-Sanitized Makefile
# -------------------------------------------------------------------

PVSNESLIB_HOME := pvsneslib
DEVKITSNES     := devkitsnes
BIN            := $(DEVKITSNES)/bin

CC      := $(BIN)/816-tcc
AS      := $(BIN)/wla-65816
LD      := $(BIN)/wlalink

ROMNAME := game
BUILD   := build
SOURCE  := main.c

# CFLAGS: -I tells tcc where C headers are
CFLAGS  := -I$(PVSNESLIB_HOME)/include -Wall -c

# ASFLAGS: -I tells the assembler where assembly includes (.inc/.asm) are
# We point it to the PVSnesLib include folder
ASFLAGS := -v -I$(PVSNESLIB_HOME)/include -I.

all: setup $(ROMNAME).sfc
	@echo "------------------------------------------------"
	@echo "FOUNDRY: ROM Baked successfully!"
	@echo "------------------------------------------------"

setup:
	@if not exist $(BUILD) mkdir $(BUILD)

# JUMP 1: C to Assembly
$(BUILD)/main.asm: $(SOURCE)
	@echo "Foundry: Performing Cross-Compilation..."
	$(CC) $(CFLAGS) $(SOURCE) -o $@

# JUMP 2: Assembly to Binary Object
$(BUILD)/main.obj: $(BUILD)/main.asm
	@echo "Foundry: Assembling Machine Code..."
	$(AS) $(ASFLAGS) -o $@ $(BUILD)/main.asm

# JUMP 3: Link Objects to ROM
$(ROMNAME).sfc: $(BUILD)/main.obj
	@echo "Foundry: Linking SNES Binary..."
	@echo [objects] > $(BUILD)/link.txt
	@echo $(BUILD)/main.obj >> $(BUILD)/link.txt
	$(LD) -v -S $(BUILD)/link.txt $@

clean:
	@if exist $(BUILD) rd /s /q $(BUILD)
	@if exist $(ROMNAME).sfc del $(ROMNAME).sfc