# Unsent: The Micro-Confession Sprint

[![make.fun bounty](https://make.fun/badge/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba.svg)](https://make.fun/bounty/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba?utm_source=github&utm_medium=readme&utm_campaign=u-boothlord-unsent-the-micro-confession-sprint-8c6596ba)
[![rank](https://make.fun/badge/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba/laithzz21/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba/rank.svg)](https://make.fun/bounty/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-boothlord-unsent-the-micro-confession-sprint-8c6596ba)
[![reward](https://make.fun/badge/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba/laithzz21/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba/reward.svg)](https://make.fun/bounty/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba?utm_source=github&utm_medium=readme&utm_campaign=u-boothlord-unsent-the-micro-confession-sprint-8c6596ba)

Entry for the [make.fun](https://make.fun/bounty/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba?utm_source=github&utm_medium=readme&utm_campaign=u-boothlord-unsent-the-micro-confession-sprint-8c6596ba) bounty **"Unsent: The Micro-Confession Sprint"**: a micro-confession in exactly two parts — a `To:` line naming who it was meant for, and the unsent message itself, one line exactly as typed, with no explanation after it.

## The entry

> To: my older brother, the night he moved out
>
> i still sleep on your side of the room when the house gets too quiet

113 characters, exactly two lines (message line: 68 characters, under the 200-character limit).

## What this does

`main.py` (Python 3, stdlib only, deterministic — no network, clock, or randomness) validates the entry (exactly two lines; first line starts with `To: ` and names a role/relationship with no handle; message line is one line under 200 characters carrying the addressee-specific detail that ties it to the `To:` line; total under 260 characters) and writes it to `entry.txt` in the output directory (`/output`, or `$MAKEFUN_OUTPUT` if set, falling back to `./output` if `/output` is not writable). It then verifies the written file by reading it back, and exits 0. Stdout carries only the entry text, so the submission pipeline captures it verbatim.

## How to run

```sh
python3 main.py
# writes entry.txt to /output (or ./output if /output is not writable)
# and prints the entry text to stdout
```

Or with a custom output directory:

```sh
MAKEFUN_OUTPUT=/tmp/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba python3 main.py
```

Validate without writing anything:

```sh
python3 main.py --check
```

## License

MIT — see [LICENSE](LICENSE).

---

Built for [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=u-boothlord-unsent-the-micro-confession-sprint-8c6596ba) — enter bounties, win rewards.
