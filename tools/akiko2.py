#!/usr/bin/env python3
"""Akiko scan, all eight address registers.

The version of this scan carried from the previous discs looked for
`lea $B80000,a0` (41f9) and `movea.l #$B80000,a6` (2c7c) only, and on Universe
that is a false negative: the CD driver loads the base into **a5** (4bf9) and
the NVRAM driver into **a2** (45f9).  A scan that fixes the address register
misses the disc.  Scan all eight forms of both instructions, always.

Reported separately, because they mean different things:

  $B80000 as a base or pointer load   the chip is being driven
  $B80004 / $B80008                   CD-ROM status and interrupt words
  $B80030                             the I2C port for the CD32's serial
                                      EEPROM -- saved games, not graphics
  $B80038 / $B8003C                   the chunky-to-planar data port
  $C0DE0000                           the Akiko identification constant

and the bare byte pattern `00 B8 00 xx`, which is reported for context only:
on this disc every one of its hits outside the two programs is a screen
x-coordinate of 184 in a hotspot table.

Usage: python3 tools/akiko2.py <file> [<file> ...]
"""
import sys, os, re, collections

# lea $xxxxxxxx.l, An   = 4?f9   for An = a0..a7
LEA = {0x41f9: 'a0', 0x43f9: 'a1', 0x45f9: 'a2', 0x47f9: 'a3',
       0x49f9: 'a4', 0x4bf9: 'a5', 0x4df9: 'a6', 0x4ff9: 'a7'}
# movea.l #$xxxxxxxx, An = 2?7c
MOVEA = {0x207c: 'a0', 0x227c: 'a1', 0x247c: 'a2', 0x267c: 'a3',
         0x287c: 'a4', 0x2a7c: 'a5', 0x2c7c: 'a6', 0x2e7c: 'a7'}

AKIKO_LO, AKIKO_HI = 0x00B80000, 0x00B80100


def u16(b, o):
    return int.from_bytes(b[o:o + 2], 'big')


def u32(b, o):
    return int.from_bytes(b[o:o + 4], 'big')


def scan(path):
    b = open(path, 'rb').read()
    loads, direct = [], []
    for o in range(0, len(b) - 6, 2):
        w = u16(b, o)
        tab = LEA if w in LEA else (MOVEA if w in MOVEA else None)
        if tab is None:
            continue
        v = u32(b, o + 2)
        if AKIKO_LO <= v < AKIKO_HI:
            loads.append((o, tab[w], v))
    for m in re.finditer(rb'\xc0\xde\x00\x00', b):
        direct.append(('C0DE0000', m.start()))
    counts = {
        'B80038': b.count(b'\x00\xb8\x00\x38'),
        'B8003C': b.count(b'\x00\xb8\x00\x3c'),
        'C0DE0000': len(direct),
        'bare 00B800xx': len(re.findall(rb'\x00\xb8\x00', b)),
    }
    return b, loads, counts


def main():
    total = collections.Counter()
    allloads = []
    for p in sys.argv[1:]:
        b, loads, counts = scan(p)
        for k, v in counts.items():
            total[k] += v
        for o, reg, v in loads:
            allloads.append((os.path.basename(p), o, reg, v))
    print('=== Akiko base/pointer loads (all 8 address registers) ===')
    if not allloads:
        print('  none')
    for name, o, reg, v in allloads:
        print('  %-24s off %6d  lea/movea $%08X, %s' % (name, o, v, reg))
    print()
    print('=== byte-pattern counts (context only) ===')
    for k in ('B80038', 'B8003C', 'C0DE0000', 'bare 00B800xx'):
        print('  %-14s %d' % (k, total[k]))


if __name__ == '__main__':
    main()
