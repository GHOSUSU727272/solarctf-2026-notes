# SolarCTF 2026 вЂ” selected analysis notebooks and scripts

Student CTF practice: signal/audio analysis, math/source-hash challenge, Android archive reversing, and memory/forensic triage. These are **selected laboratory artifacts**, not a full solve set.

**Participation:** 17 October 2026, team result reported as rank 87 (1600 points). The scripts were used during the event; their presence does not imply that every challenge was solved.

| Challenge | Topic | Outcome |
| --- | --- | --- |
| Ventilator303 | Audio signal decoding and bitstream inspection | Flag confirmed during event |
| Zero Report | Python source-hash and deterministic generator | Flag confirmed during event |
| Neuropet | Android unpacking, backup file analysis, XOR investigation | Investigation in progress |
| Task Void | Forensic recovery experiments | Investigation in progress |
| Forensics17 | Malware strings and triage helpers | Investigation in progress |

The original challenge binaries, APKs, recordings, archives, private sessions, tokens, and collected personal data are deliberately excluded. Some scripts contain challenge-specific absolute file paths and need adaptation to a fresh lab directory. Only execute them on authorized files. This repository is an honest record of experiments, including partial work.

## Reproducing
Use Python 3.12+. For audio helpers install `numpy`. Place authorized challenge inputs locally and update the path variables in each script. Scripts are provided for educational analysis rather than as a turnkey solver.

Scripts are named with their challenge prefix (for example, `zero-report__pack.py`).

