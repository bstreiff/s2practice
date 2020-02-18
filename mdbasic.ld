/*
 * Very basic linker script for the Sega Genesis/Mega Drive.
 *
 * This script is insufficient for describing a full C/C++ program,
 * but is enough for us to build an .elf file we can use for patching.
 */

OUTPUT_ARCH(m68k)
SEARCH_DIR(.)

MEMORY
{
	rom    : ORIGIN = 0x00000000, LENGTH = 0x00400000
	ram    : ORIGIN = 0x00FF0000, LENGTH = 0x00010000
}

SECTIONS
{
	.text 0x00000000 :
	{
		*(.text.*) *(.text)
		. = ALIGN(0x4);
		*(.rodata .rodata.*)
		. = ALIGN(0x4);
	} > rom

	.bss 0x00FF8000 + SIZEOF(.data) :
	{
		*(.shbss)
		*(.bss .bss.*)
		*(COMMON)
	} > ram

	/* discard */
	/DISCARD/ :
	{
		*(.stab)
		*(.strtab)
		*(.stabstr)
		*(.note)
		*(.note.*)
	}
}
