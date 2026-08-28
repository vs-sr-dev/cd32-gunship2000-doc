#!/usr/bin/env python3
"""The three figures, per file: on disc, resident, actually used.

Platform notes, section 10.  Any claim about how big a CD32 game is has to say
which of three numbers it is about:

  on disc    the bytes of the file in the ISO 9660 volume
  resident   the bytes after every packed stream inside it has been unpacked,
             at every nesting level -- for Universe that is up to three levels
             of RNC, so a naive one-level unpack understates it
  used       resident minus the trailing zeros of each unpacked blob, i.e. how
             much of the resident image is not buffer slack

Usage:
    python3 tools/band.py <iso-dir> <unpacked-dir>
"""
import sys, os


def used_of(b):
    i = len(b)
    while i and b[i - 1] == 0:
        i -= 1
    return i


def leaves(root):
    """Blobs with nothing packed inside them -- the fully expanded content."""
    out = []
    for r, _d, fs in os.walk(root):
        for f in fs:
            p = os.path.join(r, f)
            if not os.path.isdir(p[:-4] + '.d'):
                out.append(p)
    return out


def main():
    iso, unp = sys.argv[1], sys.argv[2]
    rows = []
    for r, _d, fs in os.walk(iso):
        for f in sorted(fs):
            p = os.path.join(r, f)
            disc = os.path.getsize(p)
            sub = os.path.join(unp, f)
            if os.path.isdir(sub):
                ls = leaves(sub)
                res = sum(os.path.getsize(x) for x in ls)
                use = sum(used_of(open(x, 'rb').read()) for x in ls)
            else:
                blob = open(p, 'rb').read()
                res, use = len(blob), used_of(blob)
            rows.append((f, disc, res, use))
    rows.sort(key=lambda r: -r[2])
    print('%-16s %10s %10s %10s %7s %7s' %
          ('file', 'on disc', 'resident', 'used', 'ratio', 'slack'))
    for f, d, r, u in rows:
        print('%-16s %10d %10d %10d %6.2fx %6.1f%%' %
              (f, d, r, u, r / d if d else 0,
               100.0 * (r - u) / r if r else 0))
    D = sum(r[1] for r in rows)
    R = sum(r[2] for r in rows)
    U = sum(r[3] for r in rows)
    print()
    print('bytes on disc   %10d  (%.2f MB)' % (D, D / 1048576.0))
    print('bytes resident  %10d  (%.2f MB)   %.2fx' % (R, R / 1048576.0, R / D))
    print('bytes used      %10d  (%.2f MB)   %.1f%% of resident' %
          (U, U / 1048576.0, 100.0 * U / R))
    print('buffer slack    %10d  (%.1f%% of resident)' % (R - U,
                                                          100.0 * (R - U) / R))


if __name__ == '__main__':
    main()
