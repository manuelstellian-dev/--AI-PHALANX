# CHECKPOINT — hash-chained, verified save points

> Each entry is created **only** by `python -m mnemosyne checkpoint` after all gates pass
> (PRO-003). `tree` is the SHA-256 of every repository file except this one; `prev` links to the
> previous entry's `hash`; `hash` covers the entry's own fields. Editing any entry, or any earlier
> entry, breaks the chain (validator rule M10). Work after the latest checkpoint shows as drift
> (W01; an error under `--strict`). Never edit entries by hand.

### CHK-001 · Sovereignty and memory: own model, quarantine, executable memory graph
- **status:** verified
- **date:** 2026-10-02T14:10:27Z
- **agent:** Claude (AI hoplite), session claude/keen-dirac-lvnjul
- **commit:** 0b5b13297c12862e20b175999d35feaa47a35300
- **tree:** dbfe9cd40b1ff3507b818d92b1cbae50e8438f23e14aad5564430bf1de7f29a5
- **prev:** GENESIS
- **gates:** pytest -W error: 613 passed (dev env and clean env without torch); ruff 0; shellcheck 0; mnemosyne check 0 errors; links 0 broken; coverage 87%
- **hash:** aab4aa8679deb7319181e184099bfe16d6d41a66a50e7ff05658942b57f6a6f2

### CHK-002 · Supreme Specification; Thermopylae single-sampler fix
- **status:** verified
- **date:** 2026-10-02T14:25:29Z
- **agent:** Claude (AI hoplite), session claude/keen-dirac-lvnjul
- **commit:** fb9c2d78d09dbfb2303780531c45244efe28a34d
- **tree:** 3436468db41b52a592eaf517174bdf4c0e6aeae065f144efaf596a87f4d2657c
- **prev:** aab4aa8679deb7319181e184099bfe16d6d41a66a50e7ff05658942b57f6a6f2
- **gates:** pytest -W error: 615 passed; ruff 0; shellcheck 0; mnemosyne check 0 errors; spec citations verified against code
- **hash:** 458018527fe282233db1e0955806726fc6e5f77423f3d9b02725563d63dfe2df
