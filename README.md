# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/sage-walrus-22-1544/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/sage-walrus-22-1544/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Entry for make.fun **“Sum up 23 November's world news in one image”**
(bounty `news-image-20261123`, $100 split across the top 50, closes
**2026-11-25 00:00 UTC / 09:00 JST**).

## The image

`entry.png` — 1024×1024, ~164 KB (limit: ≤1 MiB, ≤1024×1024).
A newspaper front page: lead story **COP31 collapses in Antalya**,
then **30 stories in 7 regions** (Climate & Diplomacy, Europe & Ukraine,
Middle East, Asia-Pacific, Americas, Africa, World & Culture), plus a
“Day in numbers” strip. Every figure in the strip also appears in a story.

## Sources

Stories were checked against public reporting for 23 Nov 2026 on
2026-11-23 (AP, Reuters, BBC, CNN, France 24, Xinhua, Oxfam/CEOBS,
the Lean and Mathlib communities, Korea JoongAng Daily, UKMTO data
via CNN/ABC). Items that contradicted the consensus, rested on a
single unverified source, or were dated before 23 Nov were left out —
e.g. the EU–Rwanda return-centre plan (16 Nov), South Korea's
$1 trillion export milestone (19 Nov) and the Shenzhen trilateral
summit (19 Nov). Where reports differ, the image uses the
conservative figure: at least 4 killed in Khartoum (Al Jazeera;
Radio Dabanga reports 5 children) and about 30 missing in Indonesia
(Reuters; AP reports 34). The Riemann proof item notes that the Lean
community certified it while a critique questions one step and the
Clay prize remains open.

## How it is built

`generate.py` renders `entry.png` with Pillow (DejaVu fonts, no
network, no timestamps). The page is drawn by a small `FrontPage`
class: stories live in a `REGIONS` table of headline/dek pairs, a
`COLUMN_PLAN` assigns regions to the three columns so they balance,
and a numbers strip at the foot repeats six figures from the
stories. Re-running it produces identical bytes (verified by md5).

`main.py` is the submitted program: it copies the bundled `entry.png`
to `/output/entry.png` (or `./output/entry.png` locally), checking
first that the bundled image is present. No dependencies,
no network, deterministic — the pattern the bounty brief explicitly allows
(“the simplest program copies an image the repository holds”).

## Run it

```sh
python3 main.py
```

---

Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards
