# Bluegrass in La Roche 2026

Bilingual (English/French) festival website, calendar generator, and printable schedule for the La Roche-sur-Foron bluegrass festival, 29 July – 2 August 2026.

**Live site:** https://kengray.github.io/laroche-bluegrass-2026/

## How it works

`data/schedule.json` and `data/venues.json` are the single source of truth for every act, time slot, venue, and bilingual description. `scripts/generate_all.py` reads both files and generates everything else:

- `index.html` — the festival website (bilingual, filterable by day/stage)
- Seven `.ics` calendar files — Festival, Camp, and Full variants, each in English and French, plus one legacy combined file for existing subscribers
- `LaRoche2026_Festival_Schedule.xlsx` — the full schedule as a spreadsheet

Nothing in those generated files should be hand-edited: any change will be overwritten the next time the script runs.

A GitHub Action (`.github/workflows/regenerate.yml`) runs `generate_all.py` automatically whenever `data/schedule.json`, `data/venues.json`, or `scripts/generate_all.py` is pushed to `main`, and commits the regenerated files straight back to the repo. This means schedule updates can be made entirely from the GitHub mobile app: edit `schedule.json`, commit, and the site and calendars update themselves within about 30 seconds.

Note: editing the workflow file itself doesn't trigger a run (it's not one of the watched paths), so a commit that only touches `regenerate.yml` needs a manual "Run workflow" trigger from the Actions tab.

## Subscribing to the calendar

Each `.ics` file can be subscribed to directly from its GitHub Pages URL, e.g. `https://kengray.github.io/laroche-bluegrass-2026/LaRoche2026-Festival.ics`. Subscribers' calendars pick up changes automatically whenever the schedule is updated.

## Confirming an update has gone live

The site footer shows a version number (`SITE_VERSION`, set at the top of `generate_all.py`). Bump it with every delivered change to the generator script, since GitHub's CDN can lag behind a push by a few minutes, a `Ctrl+Shift+R` only clears the local browser cache, not the CDN, so the footer version is the reliable way to confirm a change has actually gone live.

## Running locally

```
pip install openpyxl
python scripts/generate_all.py
```

No other dependencies are needed; the ICS generation uses only Python's built-in `datetime` library.

## Repo layout

```
data/
  schedule.json     bands, times, stages, bilingual notes
  venues.json       venue addresses, place IDs, verified Google Maps links
scripts/
  generate_all.py   the only script that should be run or edited
favicon/            site favicon set (SVG source + generated PNGs/ICO)
index.html          generated — do not hand-edit
*.ics, *.xlsx        generated — do not hand-edit
```

`festival_v2.py` and `generate_ics.py` at the repo root are earlier, now-superseded versions of the generator, kept for reference but no longer used by anything. Worth removing in a future tidy-up commit.
