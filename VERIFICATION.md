# Verification

Completed September 7, 2026 on Linux with Python 3.14.

- Live HTTPS download from the linked YouGov tracker endpoint succeeded.
- Parsed 84 published tracker dates from the overall registered-voter sheet.
- Latest downloaded tracker date: August 31, 2026. Workbook cells CG2–CG5 contain 0.38 approve, 0.60 disapprove, 0.02 not sure, and 1437 unweighted base; CLI displays 38%, 60%, 2%, and 1437. These are a dated verification observation, not bundled current data.
- Live history text output and offline JSON output succeeded.
- Five automated tests passed: published value conversion; rejected malformed/schema/percentage/missing data; cache fallback and offline no-network behavior; absent cache; corrupt cache.
- Temporary-prefix installation, executable launch, refusal to overwrite, uninstall, repeated uninstall, and paths containing spaces passed.
- POSIX shell syntax checks passed for both scripts.

No system-wide installation or distribution matrix testing was performed. Python 3.8 is the supported minimum based on APIs used; execution was verified on Python 3.14. The source endpoint can change independently of this app.
