"""Alien Field Notes: The Two Day Earth Review (make.fun bounty).

A tiny pure-stdlib program. It writes one original line -- an alien
tourist's two-day review of planet Earth -- to entry.txt.

The line: a visitor who loved the sunsets, could not drink the oceans,
and could not get over the locals paying rent to live on their own
planet. Verdict 2/5, would not rebook. Deterministic: every run writes
identical bytes. Standard library only; no network, no secrets.

Why this line: ten candidates were judged against the brief (alien
voice first, then funniness from the alien angle, originality, a real
review shape, tightness). The rent line won: it is the one observation
no Earth local would make about their own planet, it carries a single
joke instead of a stack, and the punch -- "would not rebook" -- lands
on the last words. Cliches cut along the way: glowing rectangles,
"take me to your leader", traffic, gravity, weather.
"""

import os

# The review: 135 characters, one line, punch lands at the end.
REVIEW = (
    "Two days on Earth: gorgeous sunsets, undrinkable oceans, and a "
    "species that pays rent to live on its own planet. "
    "2/5, would not rebook."
)

OUTPUT_NAME = "entry.txt"
MAX_LENGTH = 200


def _emit(path):
    """Write the review line to *path*, exactly one line + newline."""
    with open(path, "w", encoding="utf-8", newline="\n") as stream:
        stream.write(REVIEW + "\n")


def _targets():
    """Candidate output paths, most specific first."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    ordered = [configured] if configured else []
    ordered.append("/output")
    ordered.append("out")
    return [os.path.join(folder, OUTPUT_NAME) for folder in ordered]


def _looks_like_review(line):
    """A tourist review closes with a verdict: a score then a rebook call."""
    tail = line.rsplit(". ", 1)[-1]
    return tail.startswith("2/5") and tail.endswith("would not rebook.")


def main():
    assert 1 <= len(REVIEW) <= MAX_LENGTH, "review must be 1-200 chars"
    assert "\n" not in REVIEW, "review must be a single line"
    assert _looks_like_review(REVIEW), "review must end in a verdict"
    failure = None
    for candidate in _targets():
        try:
            folder = os.path.dirname(candidate)
            if folder:
                os.makedirs(folder, exist_ok=True)
            _emit(candidate)
            return
        except OSError as exc:  # e.g. /output not writable here; try next
            failure = exc
    raise RuntimeError(f"could not write {OUTPUT_NAME}: {failure}")


if __name__ == "__main__":
    main()
