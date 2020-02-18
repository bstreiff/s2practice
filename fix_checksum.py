#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# Fixes up the header checksum for a Genesis game. Necessary if
# the game verifies its checksum.

import argparse
import struct


def main():
    parser = argparse.ArgumentParser(description='Genesis ROM Checksum Fixer')
    parser.add_argument('--input', '-i', help='Source ROM File')
    parser.add_argument('--output', '-o', help='Output ROM File')
    args = vars(parser.parse_args())

    # Now, apply it to the ROM file
    with open(args['input'], 'rb') as input:
        # Just read the whole thing into memory. If the machine
        # is modern enough to run gcc and python3, it can probably
        # read a whole Genesis ROM into memory.
        rom = bytearray(input.read())

        # The checksum starts at the end of the header (0x200),
        # and ends at the end address of the ROM
        chk_start = 0x200
        chk_end = struct.unpack(">L", rom[0x1A4:0x1A8])[0]
        checksum = 0x0000

        addr = chk_start
        while addr < chk_end:
            checksum = checksum + struct.unpack(">H", rom[addr:addr+2])[0]
            checksum = checksum & 0xFFFF
            addr = addr + 2

        # checksum is a word at 0x18E
        rom[0x18E:0x190] = struct.pack(">H", checksum)

    with open(args['output'], 'wb') as output:
        output.write(bytes(rom))


if __name__ == '__main__':
    main()
