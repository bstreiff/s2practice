# this is what the Steam collection calls the Sonic 2 ROM
SOURCE_ROM?=SONIC2_W.68K
OBJDIR := obj
TARGET_ROM?=$(OBJDIR)/s2practice.bin
PYTHON3=python3
CC=m68k-linux-gnu-gcc
ACTIVATE_VENV=. $(OBJDIR)/venv/bin/activate

SOURCE_ASM := s2practice.S

OBJS :=	$(TARGET_ROM)

all: $(OBJS)

$(OBJS): | $(OBJDIR)

$(OBJDIR):
	@mkdir -p $(OBJDIR)

$(OBJDIR)/venv/pyvenv.cfg: requirements.txt
	@echo "Creating virtualenv..."
	@$(PYTHON3) -m venv $(OBJDIR)/venv
	@echo "Installing prereqs..."
	@. $(OBJDIR)/venv/bin/activate && pip3 -q install -r requirements.txt

clean:
	rm -rf $(OBJDIR)/

$(OBJDIR)/patches.elf: $(SOURCE_ASM) mdbasic.ld
	@echo "Compiling patch .S -> .elf"
	@$(CC) -g -O0 -T mdbasic.ld -nostdlib -ffreestanding -m68000 -Wa,--bitwise-or -Wa,--register-prefix-optional -Wl,--oformat -Wl,elf32-m68k -Wl,--build-id=none -Iinclude $(SOURCE_ASM) -o $@

$(TARGET_ROM).unchecked: $(OBJDIR)/venv/pyvenv.cfg $(OBJDIR)/patches.elf apply_patches.py
	@echo "Patching into $@"
	@$(ACTIVATE_VENV) && python3 apply_patches.py -p $(OBJDIR)/patches.elf -i $(SOURCE_ROM) -o $@

$(TARGET_ROM): $(OBJDIR)/venv/pyvenv.cfg $(TARGET_ROM).unchecked
	@echo "Updating checksum into $@"
	@$(ACTIVATE_VENV) && python3 fix_checksum.py -i $(TARGET_ROM).unchecked -o $@
