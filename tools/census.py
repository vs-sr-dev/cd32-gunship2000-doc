#!/usr/bin/env python3
"""Compression census over the extracted files.

For every file: the container magic, the RNC header fields, whether the
stream decodes and its CRC checks, and the three sizes the platform notes
ask for -- bytes on disc, bytes unpacked, and bytes actually used (the
offset of the last non-zero byte of the unpacked buffer, plus one).

Usage:  python3 tools/census.py EXTRACTDIR [--out UNPACKDIR]
"""
import os, sys, argparse, importlib.util

_spec = importlib.util.spec_from_file_location(
    "rnc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "rnc.py"))
rnc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rnc)

MAGIC = [
    (b'RNC\x01', 'RNC ProPack method 1'),
    (b'RNC\x02', 'RNC ProPack method 2'),
    (b'IMP!', 'Imploder'),
    (b'ATN!', 'Imploder (ATN!)'),
    (b'\x00\x00\x03\xf3', 'AmigaDOS hunk executable'),
    (b'\x00\x00\x03\xe7', 'AmigaDOS hunk unit'),
    (b'CrM!', 'CrunchMania'),
    (b'CrM2', 'CrunchMania 2'),
    (b'Crb!', 'CrunchMania (b)'),
    (b'PP20', 'PowerPacker 2.0'),
    (b'\x1f\x8b', 'gzip'),
    (b'x\x9c', 'zlib'),
    (b'FORM', 'IFF'),
    (b'P60A', 'The Player 6.0A module'),
    (b'DNLD', 'DNLD overlay (Dragonstone)'),
]


def identify(d):
    for m, name in MAGIC:
        if d[:len(m)] == m:
            return name
    return 'none'


def entropy(b):
    """Shannon entropy in bits/byte over the whole file.  The platform notes
    call for this on every file: a hunk executable above 7.5 is packed
    whatever its first four bytes say."""
    if not b:
        return 0.0
    import math
    c = [0] * 256
    for x in b:
        c[x] += 1
    n = float(len(b))
    return -sum((k / n) * math.log(k / n, 2) for k in c if k)


def last_used(b):
    i = len(b)
    while i > 0 and b[i - 1] == 0:
        i -= 1
    return i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--out")
    a = ap.parse_args()
    rows = []
    tot_disc = tot_unp = tot_used = 0
    for root, _, names in os.walk(a.dir):
        for n in sorted(names):
            p = os.path.join(root, n)
            rel = os.path.relpath(p, a.dir).replace('\\', '/')
            d = open(p, 'rb').read()
            kind = identify(d) if d else 'EMPTY FILE'
            unp = used = None
            note = ''
            if d[:3] == b'RNC':
                h = rnc.info(d)
                note = ("m%d ulen=%d plen=%d leeway=%d chunks=%d" %
                        (h['method'], h['unpacked'], h['packed'], h['leeway'], h['chunks']))
                try:
                    out = rnc.unpack(d)
                    unp = len(out)
                    used = last_used(out)
                    note += "  CRC ok"
                    if a.out:
                        q = os.path.join(a.out, rel)
                        os.makedirs(os.path.dirname(q) or '.', exist_ok=True)
                        open(q, 'wb').write(out)
                except Exception as e:
                    note += "  FAIL: %s" % e
            tot_disc += len(d)
            if unp:
                tot_unp += unp
                tot_used += used
            rows.append((rel, len(d), kind, unp, used, note, entropy(d)))
    print("%-24s %9s %-26s %6s %9s %9s %6s  %s" %
          ("file", "on disc", "container", "H b/B", "unpacked", "used", "use%", "notes"))
    for rel, sz, kind, unp, used, note, h in rows:
        pct = "" if not unp else "%.1f%%" % (100.0 * used / unp)
        print("%-24s %9d %-26s %6.3f %9s %9s %6s  %s" %
              (rel, sz, kind, h, unp if unp else "", used if used is not None else "", pct, note))
    print()
    print("files                 %d" % len(rows))
    print("packed (RNC)          %d" % sum(1 for r in rows if r[2].startswith('RNC')))
    print("packed (PowerPacker)  %d   -- see tools/pp20.py; RNC totals below stay 0"
          % sum(1 for r in rows if r[2].startswith('PowerPacker')))
    hi = [r for r in rows if r[6] > 7.5]
    print("entropy > 7.5 b/B     %d  %s" % (len(hi), ", ".join(r[0] for r in hi)))
    print("bytes on disc         %d" % tot_disc)
    print("bytes unpacked (RNC)  %d" % tot_unp)
    print("bytes used (RNC)      %d  (%.1f%% of unpacked)" %
          (tot_used, 100.0 * tot_used / tot_unp if tot_unp else 0))


main()
