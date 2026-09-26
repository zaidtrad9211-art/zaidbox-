# Spec: Quran circle tracker (Juz Amma) — for handing to Codex or another agent

A working v1 already exists in this folder (`index.html`, vanilla JS, no build step). Extend it; don't rewrite it.

## Users and context
- One teacher (Afnan) teaches children Quran at a center every **Saturday and Monday**.
- She tracks, per student: attendance, which surah of **Juz Amma** (surahs 78–114, 37 surahs) they recited that day, the result, and a note.
- Arabic UI, RTL, phone first. No accounts and no server: data lives in `localStorage` under key `quran-circle-v1`.

## Data model (`localStorage["quran-circle-v1"]`)
```json
{
  "students": [{"id":"str","name":"str","guardian":"str","phone":"str","notes":"str",
                "surahs":{"114":"done","113":"learning"}}],
  "sessions": {"2026-09-26": {"<studentId>": {"present":true,"surah":"113","result":"done|learning|review","note":"str"}}}
}
```

## Rules already implemented
- Warning when a student has **3 consecutive absences** (`WARN_AFTER` constant): counted over recorded sessions, newest first, stops at the first "present".
- Saving a session with result `done` marks that surah memorized. `learning` never downgrades a memorized surah.
- Memorization order is 114 → 78 (An-Nas first).
- Import students from Excel/CSV (SheetJS from jsDelivr, loaded on demand): first text cell = name, first phone-like cell = phone, header row skipped, duplicates skipped.
- Export an Excel report (Summary sheet plus Session log sheet), with a CSV fallback when offline.
- JSON backup/restore, shared through the Web Share API.
- PWA: `manifest.webmanifest` plus a network-first `sw.js`.

## Possible next tasks
1. Load the real student list from the Excel file the user will send.
2. Optional: warn on total absences in the month as well as consecutive ones.
3. Optional: an ayah-level progress note for long surahs (An-Naba, An-Nazi'at, Abasa).
4. Optional: package as an Android APK with Capacitor, the same way the root project does it (see `/.github/workflows/android.yml`).
