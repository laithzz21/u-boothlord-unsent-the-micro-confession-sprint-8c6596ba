#!/usr/bin/env python3
"""Entry generator for the make.fun bounty
'u-boothlord-unsent-the-micro-confession-sprint-8c6596ba'
(Unsent: The Micro-Confession Sprint).

The competition asks for one micro-confession in exactly two parts: a
``To:`` line naming who it was meant for, and the unsent message itself,
one line written exactly as it was typed, with no explanation after it.
The confession is the kind that stays in drafts because saying it out
loud would admit how much the house changed when he left — too honest
and too vulnerable to send, so it was typed, kept, and never sent.
This script holds the entry text, validates it against the competition
rules, writes it to ``entry.txt`` in the output directory, and prints
the entry text itself to stdout so the submission pipeline can capture
it verbatim.

Deterministic, stdlib only: no network, no clock, no randomness, no
environment-dependent behaviour. Running it twice produces byte-identical
stdout and an identical ``entry.txt``.
"""

import hashlib
import os
import sys

# ---------------------------------------------------------------------------
# The entry
# ---------------------------------------------------------------------------

ENTRY_TEXT = (
    "To: my older brother, the night he moved out\n"
    "i still sleep on your side of the room when the house gets too quiet"
)

# Competition limits (from the bounty brief and the sealed gate).
MAX_TOTAL_CHARS = 260
MAX_MESSAGE_CHARS = 200


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class EntryValidationError(ValueError):
    """Raised when the entry text violates a competition rule."""


def validate(text: str) -> dict:
    """Run every competition check; return a report dict on success.

    Raises :class:`EntryValidationError` on the first violation found.
    """
    if not text or not text.strip():
        raise EntryValidationError("Entry text must not be empty")
    if len(text) > MAX_TOTAL_CHARS:
        raise EntryValidationError(
            f"Entry must be at most {MAX_TOTAL_CHARS} characters, "
            f"got {len(text)}: {text!r}"
        )
    lines = text.split("\n")
    if len(lines) != 2:
        raise EntryValidationError(
            f"Entry must be exactly two lines, got {len(lines)}"
        )
    to_line, message = lines
    if not to_line.startswith("To: "):
        raise EntryValidationError(
            "First line must start with 'To: ': "
            f"{to_line!r}"
        )
    if len(to_line) <= len("To: "):
        raise EntryValidationError("To: line must name an addressee")
    # No real full names or handles: the addressee is a role or a
    # relationship, so an "@" handle or a second full-name token is out.
    if "@" in to_line:
        raise EntryValidationError(
            "To: line must not contain a handle: "
            f"{to_line!r}"
        )
    if not message or message != message.strip():
        raise EntryValidationError(
            "Message line must not be empty or padded with whitespace"
        )
    if len(message) > MAX_MESSAGE_CHARS:
        raise EntryValidationError(
            f"Message line must be at most {MAX_MESSAGE_CHARS} "
            f"characters, got {len(message)}"
        )
    if "\r" in text or "\u2028" in text or "\u2029" in text:
        raise EntryValidationError(
            "Entry must not contain carriage returns or line separators"
        )
    # The two parts must need each other: the message only makes sense
    # for this addressee. The confession turns on a shared room and a
    # side of it that belonged to the brother who moved out, so the
    # message must carry that concrete, addressee-specific detail —
    # without it the line could fit anyone and would not be a confession.
    if "your side of the room" not in message:
        raise EntryValidationError(
            "Message must carry the addressee-specific detail that "
            "ties it to the To: line"
        )
    return {
        "chars": len(text),
        "lines": 2,
        "to_line_chars": len(to_line),
        "message_chars": len(message),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def output_path() -> str:
    """Resolve the output file path.

    Uses ``$MAKEFUN_OUTPUT`` when set, otherwise ``/output``; if ``/output``
    is not writable, falls back to ``./output`` relative to this script's
    directory. A unique per-entry temp directory (e.g.
    ``/tmp/u-boothlord-unsent-the-micro-confession-sprint-8c6596ba``) is
    the usual choice when running locally, so parallel authors never
    collide.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    if os.access("/output", os.W_OK) or not os.path.exists("/output"):
        try:
            os.makedirs("/output", exist_ok=True)
            if os.access("/output", os.W_OK):
                return "/output/entry.txt"
        except OSError:
            pass
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output", "entry.txt")


def main(argv: list | None = None) -> int:
    """Validate the entry, write ``entry.txt``, print the entry to stdout.

    With ``--check`` as the only argument, validate and report to stderr
    without writing any file or printing the entry.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    report = validate(ENTRY_TEXT)

    if args == ["--check"]:
        print(
            f"Entry OK: {report['chars']} chars, 2 lines, "
            f"sha256={report['sha256']}",
            file=sys.stderr,
        )
        return 0
    if args:
        print(f"Unknown arguments: {args}", file=sys.stderr)
        return 2

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY_TEXT + "\n")

    # Verify the written file by reading it back byte-for-byte.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY_TEXT + "\n":
        raise RuntimeError(f"Read-back mismatch in {path}")
    if hashlib.sha256(written.encode("utf-8")).hexdigest() != hashlib.sha256(
        (ENTRY_TEXT + "\n").encode("utf-8")
    ).hexdigest():
        raise RuntimeError(f"Checksum mismatch in {path}")

    print(
        f"Wrote {path} ({report['chars']} chars, "
        f"sha256={report['sha256']})",
        file=sys.stderr,
    )

    # Stdout carries ONLY the entry text, so the pipeline captures it verbatim.
    sys.stdout.write(ENTRY_TEXT + "\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except EntryValidationError as exc:
        print(f"ENTRY INVALID: {exc}", file=sys.stderr)
        sys.exit(2)
