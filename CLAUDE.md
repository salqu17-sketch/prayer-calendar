# Prayer Calendar Generator — project context

Handoff from a Claude chat session (2026-10-12 → 2026-11-02). The user is Salman (Riyadh); he writes in Arabic. Reply in elevated Classical Arabic (فصحى), begin every reply with "Bismellah.", answer first, no filler.

## What this repo is
- `index.html`: a single self-contained page (no build, no server, no network calls). The user picks country/city (or uses device location), a date range, and per-prayer event durations, then downloads an `.ics` file of prayer times.
- Served via GitHub Pages from `main` / root: https://salqu17-sketch.github.io/prayer-calendar/ (the user enables Pages himself; the earlier session could not).
- A twin copy is published as a private claude.ai artifact (https://claude.ai/artifact/SJVCa1YT1iQaEn8Z4snert). It differs only at runtime: inside Claude, the page saves a `.zip` that wraps the `.ics` via the artifact `downloads` capability (`.ics` is not on that allowlist), hides the location button (device APIs are refused there), and shows a copy-text fallback. Detected with `IN_CLAUDE = !!(window.claude && window.claude.use)`.

## Settled decisions (do not change without asking)
- Event titles carry emoji: 🌅 الفجر, ☀️ الظهر, 🌤️ العصر, 🌇 المغرب, 🌙 العشاء. On Fridays Dhuhr becomes 🕌 الجمعة.
- Default durations from adhan: Fajr 40, Dhuhr 30, Jumuah 50, Asr 30, Maghrib 20, Isha 30 min. They are editable in the page and saved in localStorage; a reset button restores the defaults.
- One 10-minute display alarm before each adhan. TRANSP:TRANSPARENT.
- Events are written in UTC (`Z`), so they are correct in any viewer time zone.
- Sunrise is deliberately excluded.
- The preview shows adhan times only. The user rejected an "end time" column, because it suggests the end of the shar'i prayer time. Do not reintroduce it.
- A day-strip chart was removed as unclear.
- The calculation method defaults by country (Umm al-Qura for KSA: Fajr 18.5°, Isha = Maghrib + 90 min, +120 min in Ramadan detected via `Intl` islamic-umalqura). Asr uses the standard (shadow = 1×) rule. High latitudes use angle-based night portions.

## Verification already done
- Riyadh output matched the Python-generated file exactly for all 1825 events (2026-10-12 → 2027-10-11).
- Spot checks against AlAdhan (method 4): Riyadh and Makkah matched; Asr occasionally runs 1 min early (a rounding difference).
- Not independently verified: the non-Saudi methods (the UAE 18.2°/18.2° value is uncertain) and high-latitude cities (e.g. London summer).

## Also done for the user (outside this repo)
- Generated yearly `.ics` files for Riyadh, Makkah and Dammam (`tools/` has the Python scripts: `generate_ics.py LAT LNG slug "اسم المدينة"`, then `set_durations.py in.ics out.ics`). The user has Google Calendar calendars named «وقوت الصلاة في الرياض», «وقوت الصلاة - مكة», «وقوت الصلاة - الدمام». He chose to delete and re-import them himself with the new durations. Updating ~4,140 events one at a time through the connector was judged too slow.

## Open items
- Confirm GitHub Pages is enabled and the live URL works.
- The iPhone "Add All" flow with a full-year file (1825 events) is untested on a real device.
