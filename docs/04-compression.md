# 04 — Compression

Reproduce with `tools/packscan.py` (inherited) and `tools/containers2.py` (new).
Results in [`notes/pack-scan.txt`](../notes/pack-scan.txt) and
[`notes/containers.txt`](../notes/containers.txt).

## The rule goes to [10 of 10]

The rule in the shared checklist is: compression on a CD32 disc correlates with
the title having had a floppy release. It stood at [9 of 9] after Universe.

Gunship 2000 has the most explicit floppy ancestor in the series
([03-boot-chain.md](03-boot-chain.md)) and it compresses. **[10 of 10].**

The prediction was written before the scan and it was right, but it is worth
saying why it was not obvious: with a 157.84 MB data track and 63.4 % of the
volume left as a zero hole, there is no space pressure of any kind on this disc.
Four discs in the series compress nothing at all. Gunship compresses anyway, and
it compresses exactly the material that came off the floppies.

## What is packed

One method, one nesting level, two files.

```
=== cd32rez (641768 bytes) ===
  depth 0:  526 streams,    616483 packed ->   1423566 unpacked
  gaps   :  270, 25285 bytes (241 all-zero, 241 bytes)
=== pirates (383568 bytes) ===
  depth 0:    8 streams,     61064 packed ->    198912 unpacked
  gaps   :    9, 322504 bytes (0 all-zero)
=== pirates_german (383724 bytes) ===
  depth 0:    8 streams,     61064 packed ->    198912 unpacked
```

**542 validated RNC ProPack method 2 streams**, every CRC-16 correct, over three
files. Nothing else on the disc is packed: the other 137 files are raw IFF, raw
hunk, raw text or raw sample data.

Re-scanning every unpacked stream found **no second level**. Universe's three
levels of RNC are not repeated here; depth is 0 throughout. That is a negative
result and it is reported as one — the re-scan was run twice, as the checklist
requires, and came back empty both times.

No PowerPacker, no Imploder, no Bytekiller, no CrunchMania, no RNC method 1, no
XOR-keyed RNC. No eighth cruncher. The scan validates by running the
decompressor at every byte offset, so a negative is a real negative for the
seven known containers.

### A note on the inherited tool

`containers.py` from `cd32-universe-doc` calls `rnc.unpack`, which is the
method-1 bit stream, because Universe packs exclusively with method 1. Run
unchanged on this disc it reports **zero streams** on a disc that has 542.
`tools/containers2.py` here tries both decoders. This is the same class of
failure as `akiko.py` on Universe: an inherited tool with a hard-coded
assumption produces a clean, confident, wrong negative. `packscan.py` was
already method-agnostic and found them, which is why the two were run side by
side.

## `cd32rez` — a resource archive that uses LoadSeg as its fixup

`cd32rez` is 641,768 bytes and begins `00 00 03 F3`, so a census calls it an
executable. It has one CODE hunk of 641,656 bytes and fifteen relocations.

All fifteen relocations point at the first 60 bytes of the hunk:

```
hunk0+0x000000 (file 0x000020) -> hunk0+0x000040
hunk0+0x000004 (file 0x000024) -> hunk0+0x007456
hunk0+0x000008 (file 0x000028) -> hunk0+0x00a310
...
hunk0+0x000038 (file 0x000058) -> hunk0+0x03047c
```

followed by `FFFFFFFF` as a terminator. So the "code" is a fifteen-entry pointer
table and the remaining 641,596 bytes are payload. The file is a resource
archive that does not implement pointer fixup at all: it declares the group
pointers as relocations and lets `LoadSeg` patch them while loading. Nothing has
to be parsed at runtime.

The first table entry, `hunk0+0x40`, is file offset 0x60 = 96, which is exactly
where the first RNC stream starts. The second, `hunk0+0x7456`, is file offset
29,814, which is exactly the second stream. The table indexes fifteen groups of
streams, not fifteen streams.

Group 3 is the exception: its pointer lands on file offset 41,776, and the
16,000 bytes from there to the start of group 4 are **raw, not packed** — the
one large unpacked run inside the container.

### The gaps

270 gaps totalling 25,285 bytes. 241 of them are a single byte, all zero: RNC
streams are aligned to even offsets and a one-byte pad appears wherever the
previous stream ended odd. The remaining 29 gaps hold 25,044 bytes, of which the
16,000-byte raw block above is the bulk. The others range from 48 to 1,761 bytes.

This matters because of Universe, where the gaps between concatenated streams
were not padding at all — they carried the resource offset tables, the hotspot
tables and the bytecode. Here they mostly are padding, and the check that
establishes it is the count of one-byte all-zero gaps: 241 of 270.

## `pirates` and `pirates_german`

The two Pirates! Gold demo executables each contain eight RNC2 streams in the
middle of the file, at identical offsets, with identical SHA-1s on the unpacked
output. 61,064 packed bytes become 198,912. Only 15.9 % of each file is packed;
the rest is ordinary hunk data.

The two files are byte-identical for their first 79 bytes and diverge inside the
hunk size table, at the declared length of hunk 14 (0x1F14 vs 0x1F1F words =
31,824 vs 31,868 bytes). Everything else about them — hunk count, hunk kinds,
memory flags, the eight packed streams, and 2,346 of the 2,374 relocations —
is the same. The German build differs only in the final DATA hunk, which is the
string table. See [11-leftovers.md](11-leftovers.md).

## Entropy

Printed because it costs nothing, not because it decides anything — Fire & Ice
established that entropy is sufficient but not necessary, hiding 29 PP20 streams
inside already-unpacked files without a single 8 KB window above 7.5 bits/byte.

On this disc entropy would have been a poor guide in the other direction: the
CDXL video is 86.9 % of the file bytes and is high-entropy delta-free image and
audio data that is not compressed at all, while `cd32rez` — which is 96.1 %
packed — is only 1.1 % of the file bytes. A whole-disc entropy sweep points at
the video and misses the archive. The magic scan validated by decompression
finds the archive and correctly ignores the video.
