#!/usr/bin/env python3
"""Prose census against both denominators (platform notes, section 9).

Universe established that "how much text" needs a denominator, and that the
two candidates differ by a factor of two: bytes on disc, and bytes of the
resident image.  Both are printed here.

"Prose" is deliberately conservative: a NUL-terminated run of at least
`--min` printable bytes that contains a lowercase letter and a space, so that
filenames, register names and hex tables do not count as text.  The point is a
floor that can be defended, not a maximum.

Usage:
    python3 tools/textcensus.py <dir> [<dir> ...] [--min N] [--max N]
                                [--dump FILE] [--per-file]
"""
import sys, os, re, argparse, collections

RUN = re.compile(rb"[\x20-\x7e\xa0-\xff]{%d,}")


def prose_runs(d, minlen):
    out = []
    for m in re.finditer(rb"[\x20-\x7e]{%d,}" % minlen, d):
        s = m.group()
        if b" " not in s:
            continue
        if not any(97 <= c <= 122 for c in s):
            continue
        # at least two words with a lowercase letter
        words = [w for w in s.split() if len(w) > 1]
        if len(words) < 2:
            continue
        out.append((m.start(), s))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--min", type=int, default=12)
    ap.add_argument("--max", type=int, default=48, help="truncate each dumped run")
    ap.add_argument("--dump")
    ap.add_argument("--per-file", action="store_true")
    a = ap.parse_args()

    tot_bytes = 0
    tot_text = 0
    tot_runs = 0
    per = []
    dump = open(a.dump, "w", encoding="utf-8") if a.dump else None
    high = collections.Counter()
    for root in a.dirs:
        for dp, dn, fn in os.walk(root):
            for f in sorted(fn):
                p = os.path.join(dp, f)
                d = open(p, "rb").read()
                tot_bytes += len(d)
                runs = prose_runs(d, a.min)
                nb = sum(len(s) for _o, s in runs)
                tot_text += nb
                tot_runs += len(runs)
                for c in d:
                    if c >= 0x80:
                        high[c] += 1
                if runs:
                    per.append((nb, len(runs), os.path.relpath(p, root).replace(os.sep, "/")))
                if dump:
                    for o, s in runs:
                        t = s.decode("latin-1")
                        if len(t) > a.max:
                            t = t[:a.max] + "..."
                        dump.write("%-30s 0x%06x  %s\n" % (os.path.basename(p), o, t))
    if dump:
        dump.close()

    print("scanned          %d bytes" % tot_bytes)
    print("prose runs       %d" % tot_runs)
    print("prose bytes      %d  (%.2f%% of the bytes scanned)"
          % (tot_text, 100.0 * tot_text / max(1, tot_bytes)))
    print("min run length   %d, must contain a space and a lowercase letter" % a.min)
    print()
    if a.per_file:
        print("%10s %6s  %s" % ("bytes", "runs", "file"))
        for nb, nr, p in sorted(per, reverse=True)[:40]:
            print("%10d %6d  %s" % (nb, nr, p))
    print()
    print("bytes >= 0x80 in the scanned set: %d distinct values, %d occurrences"
          % (len(high), sum(high.values())))
    for v, n in high.most_common(12):
        print("   0x%02X x%d" % (v, n))


if __name__ == "__main__":
    main()
