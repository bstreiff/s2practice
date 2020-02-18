#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# Applies "patches" bounded by symbols in a ELF file.
# Each region to patch should start with a symbol prefixed with "__patch$",
# and will end with a symbol prefixed with "__endpatch$". The suffixes
# are not used, but do need to be unique to not have symbol collisions.

import argparse
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection


class Patch(object):
    def __init__(self, section_index, start_addr, end_addr):
        self.section_index = section_index
        self.start_addr = start_addr
        self.end_addr = end_addr
        self.data = None


def collect_patches(patchfile):
    with open(patchfile, 'rb') as file:
        elf = ELFFile(file)

        symbol_tables = [s for s in elf.iter_sections()
                        if isinstance(s, SymbolTableSection)]

        patches = []

        # Gather symbols.
        for section in symbol_tables:
            # We need to find the length of each patched section. However,
            # because these are annotated using symbols, symbols have no
            # length and thus we can't look at st_size. Instead, we define
            # pairs of symbols (using "patch" and "endpatch" macros),
            # and use those to find the length of each patch.

            # Get all the "start" and "end" symbols, in sorted order.
            patch_start_syms = sorted([s for s in section.iter_symbols()
                                       if s.name.startswith("__patch$")],
                                      key=lambda x: x['st_value'])
            patch_end_syms = sorted([s for s in section.iter_symbols()
                                     if s.name.startswith("__endpatch$")],
                                    key=lambda x: x['st_value'])

            for symbol in patch_start_syms:
                section_index = symbol['st_shndx']
                start_addr = symbol['st_value']
                # For this "start" symbol, get the closest "end".
                closest = next(filter(lambda x: start_addr < x['st_value'],
                                      patch_end_syms))
                # Get the length, and store it in the array.
                end_addr = closest['st_value']
                patches.append(Patch(section_index, start_addr, end_addr))

        # Now, retrieve data.
        for patch in patches:
            section = elf.get_section(patch.section_index)
            data = section.data()[patch.start_addr:patch.end_addr]
            patch.data = data

    return patches


def main():
    parser = argparse.ArgumentParser(description='ROM Patcher')
    parser.add_argument('--input', '-i', help='Source ROM File')
    parser.add_argument('--patch', '-p', help='Compiled Patches')
    parser.add_argument('--output', '-o', help='Output File')
    args = vars(parser.parse_args())

    patches = collect_patches(args['patch'])

    # Now, apply it to the ROM file
    with open(args['input'], 'rb') as input:
        with open(args['output'], 'wb') as output:
            # Just read the whole thing into memory. If the machine
            # is modern enough to run gcc and python3, it can probably
            # read a whole Genesis ROM into memory.
            rom = bytearray(input.read())

            for patch in patches:
                rom[patch.start_addr:patch.end_addr] = patch.data

            output.write(bytes(rom))


if __name__ == '__main__':
    main()
