# 06 — Text

Reproduce with `tools/textcensus.py` and `tools/strdump.py`. Census in
[`notes/text-census.txt`](../notes/text-census.txt).

## The figure, and the denominator

Universe filled this section for the first time and established that "how much
text" is meaningless without saying which denominator, because the two candidates
differ by a factor of two. Both are given here.

```
scanned          59,789,206 bytes (the 140 files as they sit on disc)
prose runs       2,925
prose bytes      104,838   = 0.18 % of the bytes scanned
```

Against the resident image (61,610,596 bytes after unpacking every stream at
every level) it is **0.17 %**. Against the game only, excluding streamed video,
the bundled second title and the stock OS binaries — 8,363,560 bytes resident —
it is **0.65 %**.

"Prose" here is a defensible floor, not a maximum: a run of at least twelve
printable bytes containing a space, a lowercase letter and at least two words of
more than one character. Filenames, register tables and hex do not qualify.

For comparison, Universe measured 602,344 bytes, 6.53 % of its resident image
and 13.70 % of its on-disc bytes. Gunship 2000 has **one sixth of Universe's
prose in absolute terms and one thirty-eighth of its share**. A flight simulator
turns out to be a text-poor genre on this evidence, and the answer is boring, but
it is boring with a number attached.

## Where the text is

```
     bytes   runs  file
     25869    631  pirates
     24084    730  pirates_german
     14984    245  object.cat
     14599    241  gs
     10946    561  gs2frt.dat
      3900    107  Catalogs/English/Ami.catalog
      1957     59  gs2.run
      1470     61  CDGSXL  (and c/cdgsxl, identical)
      1140     58  INTRO.XL
      1016     42  c/setpatch
       554     20  gunship 2000
       536     13  s/startup-sequence
       375     17  Backdrop
       307      5  pirates.demo
       263     12  c/execute
       140      7  roster.dat
```

**The largest body of prose on the disc belongs to the game that never runs.**
`pirates` and `pirates_german` hold 49,953 bytes between them — 47.6 % of all
prose on the disc — and neither is ever launched
([11-leftovers.md](11-leftovers.md)).

Excluding those two, Gunship 2000's own text is 54,885 bytes, and the largest
single share of it is inside the 3D models.

## There is no string table

The three parser traps catalogued on Universe — an unstored table length,
entries that point backwards to reuse a line, and two record shapes distinguished
only by whether the first byte is printable — do not apply here, because there is
no string table to parse. Every string on this disc is a NUL-terminated run
embedded where it is used:

* `object.cat` stores each model's name and description inside the `.SBN` file.
* `gs` stores its error and UI strings inline in DATA hunks.
* `gs2frt.dat` stores screen labels inside the little-endian IFF chunks.
* The two locale catalogues are standard IFF `CTLG`.

That is a negative result and it is worth stating plainly: a scan that assumed
Universe's model would have found nothing and concluded the text was compressed.
Here a flat `strings`-equivalent pass is the correct model, and the number it
produces is the number.

Because there is no table, there are no empty slots to count. The Universe
technique of diffing parallel copies of a table and printing the indices that
are empty in N-1 of N has nothing to work on.

## Encoding

```
bytes >= 0x80 in the ISO tree: 128 distinct values, 798,248 occurrences
```

Every one of those is inside binary payload — packed streams, IFF BODY data,
CDXL frames, sample data. **No prose run on this disc contains a byte above
0x7F.** The English text is 7-bit ASCII throughout.

The German build of the Pirates! Gold demo is also 7-bit: `vielversprechende`,
`Abenteurer`, `Schaluppe`, `Kriegsgaleone`, `Frankreich` — German needs umlauts
and this text has none where it would want them, which is the "accents simply
removed" case already seen in the series rather than a new encoding.

No XOR key was needed and none was found: a candidate scan over all 256 keys was
unnecessary because the plain scan already returns as much prose as the game
plausibly shows.

## Localisation, such as it is

`/Catalogs/English/` holds two IFF `CTLG` files and there is no second language
directory. `Ami.catalog` (5,046 bytes, `$VER: Ami.catalog 1.00 (22.03.94)`,
`LANG english`) is not game text at all — it is a developer-facing error
catalogue for an internal toolkit called *Ami*:

```
Not enough data memory for queue
Can't allocate signal for queue
Can't open %s version %ld
Not enough free graphics memory in system
Can't open .info file
Can't wait for input with no display open
Can't get drawing buffer bitmap with no display open
Can't get clearing buffer bitmap with no display open
Can't get viewing buffer bitmap with no display open
Can't set palette with no display open
```

The three-buffer vocabulary — drawing, clearing, viewing — describes a
triple-buffered display abstraction. `Backdrop` is the program that opens
`locale.library` and would read this catalogue. An internal framework's
diagnostic messages, localised, shipped on a retail disc.

`User.catalog` is 166 bytes, `$VER: ami.catalog 1.00 (15.2.94)` — note the
lowercase `ami` where the other says `Ami`, and a date five weeks earlier.

## Version strings

Seven `$VER:` strings on the disc, none of them in a game program:

```
c/setpatch          $VER: setpatch 40.14 (7.10.93)
c/Assign            $VER: assign 37.4 (25.4.91)
c/execute           $VER: execute 37.11 (14.5.91)
c/wait              $VER: wait 37.3 (5.4.91)
c/Status            $VER: status 37.2 (1.4.91)
c/Break             $VER: break 37.1 (10.1.91)
c/avail             $VER: avail 37.2 (21.1.91)
CDGSXL              $VER: cdgsxl 1.50 (15.10.93) Wayne D. Lutz
Ami.catalog         $VER: Ami.catalog 1.00 (22.03.94)
User.catalog        $VER: ami.catalog 1.00 (15.2.94)
frame.lbm           $VER: Written by ASDG's Art Department Professional IFF3.0.4 (02.12.93)
```

Three things come out of that list. The AmigaDOS commands are all 37.x —
Workbench 2.0 — while SetPatch is 40.14, Workbench 3.1: a 3.1 SetPatch dropped
into an otherwise 2.0 `C:` directory. The CDXL player is third-party and names
its author, **Wayne D. Lutz**, the only person named anywhere on this disc.
And `frame.lbm` carries an ASDG Art Department Professional annotation, which
names the paint package one asset went through.

The game's own version comes from a bare banner with no `$VER:` prefix, in the
launcher at file offset 0xae6:

```
Gunship 2000     V3.32 - 15/4/1994
```

Third bare banner in the series after Banshee (23 bytes between an `rts` and the
next routine) and Fire & Ice (a line inside a diagnostic panel). Unlike Universe,
which had neither and had to be dated from the timestamp log alone, this disc
dates itself.
