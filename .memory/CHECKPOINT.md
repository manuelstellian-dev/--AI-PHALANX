# CHECKPOINT — hash-chained, verified save points

> Each entry is created **only** by `python -m mnemosyne checkpoint` after all gates pass
> (PRO-003). `tree` is the SHA-256 of every repository file except this one; `prev` links to the
> previous entry's `hash`; `hash` covers the entry's own fields. Editing any entry, or any earlier
> entry, breaks the chain (validator rule M10). Work after the latest checkpoint shows as drift
> (W01; an error under `--strict`). Never edit entries by hand.
