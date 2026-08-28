# 01 — The disc image

Reproduce with `tools/isodump.py` and `tools/cueaudio.py`.

## Tracks

```
CATALOG 5015352330281
TRACK 01  MODE1/2048  80,813 sectors in the image, 80,735 declared
TRACK 02  AUDIO       PREGAP 00:02:00   9,784 frames   2:10.34
TRACK 03  AUDIO                        18,103 frames   4:01.28
TRACK 04  AUDIO       INDEX 00/01      18,232 frames   4:03.07
TRACK 05  AUDIO       INDEX 00/01      17,560 frames   3:54.10
TRACK 06  AUDIO       INDEX 00/01       6,457 frames   1:26.07
```

Audio total 70,136 frames, 15:35.11, all 44,100 Hz 16-bit stereo, all five
distinct by SHA-1. Data 80,813 + audio 70,136 = 150,949 sectors = 45.3 % of a
333,000-sector CD. Data is 53.5 % of that and audio 46.5 %: the first disc in
this series where the data track is the larger half.

The CATALOG is a real EAN-13, not the thirteen zeros four discs in the series
carry.

## The one-frame pregap on tracks 4, 5 and 6 is not describing the audio

Tracks 4, 5 and 6 declare `INDEX 00 00:00:00` and `INDEX 01 00:00:01` — a
one-frame pregap **inside the file**. Tracks 2 and 3 declare only `INDEX 01`.
No other cue in this series shows this.

It corresponds to nothing in the image. Measured leading digital silence:

| track | declared pregap | measured leading silence |
|---|---|---|
| 2 | none (2 s generated) | 23,472 bytes = 9 frames |
| 3 | none | 24,728 bytes = 10 frames |
| 4 | 1 frame | 29,012 bytes = 12 frames |
| 5 | 1 frame | 30,976 bytes = 13 frames |
| 6 | 1 frame | 31,740 bytes = 13 frames |

Every track opens with 9 to 13 frames of digital silence whether or not the cue
declares an INDEX 00, and no track's silence is one frame long. The declared
pregap is a cue-sheet artefact of whatever produced this rip; it is not a
boundary present in the audio. Recorded as a negative result.

`PREGAP 00:02:00` on track 2 is the ordinary 150-frame data-to-audio gap and is
generated rather than stored, as on every other disc in the series.

## Sector map

```
LBA        0 ..     15   system area                    16 sectors
LBA       16 ..     16   primary volume descriptor
LBA       17 ..     17   duplicate of sector 16 (byte-identical)
LBA       18 ..     18   volume descriptor set terminator
LBA       19 ..     20   path tables (M then L)
LBA       21 ..     21   .TM trademark block
LBA       22 ..     24   root directory, 6,144 bytes
LBA       25 ..  51,224  UNCLAIMED, 51,200 sectors, all zero    <-- 100 MiB
LBA   51,225 ..  80,502  filesystem: 9 directories, 140 files
LBA   80,503 ..  80,734  UNCLAIMED, 232 sectors, all zero
LBA   80,735 ..  80,812  image overrun past the declared volume, 78 sectors, all zero
```

## The 100 MiB hole

```
LBA 25..51224: 104857600 bytes, 0 non-zero
sha1 2c2ceccb5ec5574f791d45b63c940cff20550f9a
== 100 MiB exactly? True
```

51,200 sectors × 2,048 = 104,857,600 bytes = **exactly 100 × 1024 × 1024**. Not
a rounded figure: the run is exactly 100 MiB and every byte of it is zero. It is
63.4 % of the declared volume and 63.4 % of the image.

This is the fourth disc in the series with a hole in front of the files:

| disc | gap before the files | share of the volume | round number? |
|---|---:|---:|---|
| Prey (CD32) | 6,000 sectors | | no |
| Microcosm | 15,000 sectors | | no |
| HeroQuest II | 24,272 sectors | 95.4 % | no |
| **Gunship 2000** | **51,200 sectors** | **63.4 %** | **yes — exactly 100 MiB** |

The reading these gaps used to get — seek optimisation for Red Book audio during
play — was already carrying four negatives (Guardian, Banshee, Fire & Ice,
Universe, the last two being the two most audio-heavy discs in the series) and is
treated as refuted. This disc adds a fifth kind of evidence against it and one
for the mastering-side explanation: a gap that is a round binary number to the
byte is a *reservation*, not a layout optimisation. Something asked for 100 MiB
and the files were placed after it. Nothing on the disc says what for; see
[12-open-questions.md](12-open-questions.md).

Note what it is not. It is not the Microcosm shape (one file that is almost the
whole disc: the largest file here is 16.2 % of the image). It is not the Prey
CDTV shape (a dump artefact past the declared end: the overrun here is 78
sectors, and the hole is *inside* the declared volume, so the mastering tool
counted it deliberately).

## The 232-sector tail

```
tail LBA 80503..80734: 475136 bytes, 0 non-zero
```

232 unclaimed sectors, all zero, exactly as predicted from the preparer field
before the filesystem was parsed. See
[12-open-questions.md](12-open-questions.md) for the state of that correlation,
which is now five for five.

## Image overrun

78 sectors past the declared volume, all zero. The values seen so far:

| disc | overrun | preparer |
|---|---:|---|
| **Gunship 2000** | **78** | **D J Pocock** |
| Universe | 80 | D J Pocock |
| Banshee | 86 | D J Pocock |
| Fire & Ice | 87 | D J Pocock |
| Liberation | 103 | D J Pocock |
| Dragonstone | 106 | Sajjad Majid |

Gunship widens the Pocock range to 78–103 and Dragonstone still sits above all
of it, so overrun still does not separate the group cleanly. Universe already
established that; this disc does not change it.
