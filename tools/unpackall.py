#!/usr/bin/env python3
"""Unpack every RNC stream on the disc, at every nesting level, into a tree.

Output layout mirrors the nesting:

    OUT/part1.dat/                     the outer stream's output
    OUT/part1.dat.d1/000002.bin        each depth-1 stream, named by its
                                       offset inside the parent
    OUT/part1.dat.d1/000002.d2/...     and so on

Gaps between streams (raw, unpacked bytes) are written alongside as
`.gapNNNNNN.bin`, because on this disc the gaps carry the resource headers and
the script data -- they are not padding.

Usage: python3 tools/unpackall.py <iso-dir> <out-dir>
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from containers import streams


def emit(blob, outdir, name):
    os.makedirs(outdir, exist_ok=True)
    ss = streams(blob)
    if not ss:
        return 0
    n = 0
    cur = 0
    for off, packed, data in ss:
        if off > cur and off - cur > 4:
            open(os.path.join(outdir, '%s.gap%06d.bin' % (name, cur)),
                 'wb').write(blob[cur:off])
        stem = '%s.%06d' % (name, off)
        open(os.path.join(outdir, stem + '.bin'), 'wb').write(data)
        n += 1
        n += emit(data, os.path.join(outdir, stem + '.d'), stem)
        cur = off + packed
    if cur < len(blob) and len(blob) - cur > 4:
        open(os.path.join(outdir, '%s.gap%06d.bin' % (name, cur)),
             'wb').write(blob[cur:])
    return n


def main():
    src, dst = sys.argv[1], sys.argv[2]
    total = 0
    for r, _d, fs in os.walk(src):
        for f in sorted(fs):
            p = os.path.join(r, f)
            blob = open(p, 'rb').read()
            n = emit(blob, os.path.join(dst, f), f)
            if n:
                print('%-14s %3d streams' % (f, n))
            total += n
    print('total %d streams' % total)


if __name__ == '__main__':
    main()
