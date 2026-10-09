# File Organizer

A dry-run-first Python file organizer with a static filename planning demo. Categories: Images, Docs, Media, Archives, Code and Others.

## Python CLI

Python 3.10+: `python3 main.py /path/to/folder` prints planned moves and changes nothing. Back up files, inspect the plan, then use `python3 main.py /path/to/folder --apply` to apply. Files are copied to exclusively-created targets, metadata copied and original removed after success. Existing destinations are never replaced; collisions get numbered.

Only regular non-symlink root files are considered. Hidden files, directories and this script are skipped. Destination symlink folders/non-folders are rejected. Use in a trusted directory without concurrent writers; this is not a transactional batch or a rollback system. An I/O failure may leave earlier moves complete; re-run a dry preview to inspect remaining work. No recursive traversal or arbitrary untrusted-folder security guarantee.

## Browser demo

Paste filenames, one per line, to classify/preview up to 200 names. Duplicate filenames in the input are numbered case-insensitively. Copy or export JSON. It never reads, uploads, renames or moves your files and cannot check actual destination collisions. It previews hidden filenames too; the CLI deliberately skips them. Theme is the only saved value.

## Tests/build

Node 22 + Python 3.10+: `npm test` runs 8 Python tests and 14 JS tests. `npm run build` creates dist plus a Python download. No install/dependency step. Browser checks cover plan/duplicates, copy/export, rejected paths, safe text rendering, clear/theme persistence and mobile overflow. Python tests cover dry preview, collision preservation, symlink/folder skips, unsafe destinations, exclusive-create races and byte preservation.

## Workflow

Typed branch, local tests/build and desktop dark/mobile visual checks, then one PR/squash to main. Production Pages only triggers on main pushes. No PR/branch/tag/manual builds. Pages Source Actions and environment main-only before merge. Dist only is deployed. Do not change profile pins.

## UI sources

Pines button styling adapted: https://devdojo.com/pines/docs/button . Discovery checked at https://shoogle.dev/ . Local Lucide icons (ISC): LICENSE-icons. No third-party scripts/fonts/assets are requested by the demo.
