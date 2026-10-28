"""Data models for PromptProof.

Only the Python standard library is used, so the tool runs anywhere
Python 3.10+ is available without an installation step.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field

ALLOWED_RESOLUTIONS = ("768P", "1080P", "2K")
MIN_DURATION_SEC = 1.0
MAX_DURATION_SEC = 15.0


@dataclass
class Shot:
    """One structured video shot.

    A free-form prompt is split into named fields on purpose: a missing
    camera move or a missing subject is easy to spot in a field, and
    almost impossible to spot in a paragraph.
    """

    id: str
    subject: str
    action: str
    camera: str = "static"
    style: str = ""
    source_image: str = ""
    negative: str = ""
    duration_sec: float = 5.0
    final_resolution: str = "2K"

    def fingerprint(self) -> str:
        """Stable hash of the creative fields, used for de-duplication.

        Duration and resolution are excluded: re-rendering the same
        creative content at another size is still a duplicate shot.
        """
        payload = "|".join(
            part.strip().lower()
            for part in (self.subject, self.action, self.camera,
                         self.style, self.source_image)
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]

    def validate(self) -> list[str]:
        """Return a list of human-readable problems; empty means valid."""
        problems: list[str] = []
        if not self.id.strip():
            problems.append("id is empty")
        if not self.subject.strip():
            problems.append(f"{self.id or '?'}: subject is empty")
        if not self.action.strip():
            problems.append(f"{self.id or '?'}: action is empty")
        if not (MIN_DURATION_SEC <= float(self.duration_sec) <= MAX_DURATION_SEC):
            problems.append(
                f"{self.id}: duration_sec {self.duration_sec} out of "
                f"range {MIN_DURATION_SEC}-{MAX_DURATION_SEC}"
            )
        if self.final_resolution not in ALLOWED_RESOLUTIONS:
            problems.append(
                f"{self.id}: final_resolution {self.final_resolution!r} "
                f"must be one of {ALLOWED_RESOLUTIONS}"
            )
        return problems

    @classmethod
    def from_dict(cls, data: dict) -> "Shot":
        known = {name for name in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})

    def to_dict(self) -> dict:
        return asdict(self)


def load_shots(path: str) -> list[Shot]:
    """Load a JSON file containing a list of shot objects."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    if not isinstance(raw, list):
        raise ValueError("input JSON must be a list of shot objects")
    return [Shot.from_dict(item) for item in raw]


def find_duplicates(shots: list[Shot]) -> dict[str, list[str]]:
    """Map fingerprint -> shot ids, keeping only groups with 2+ shots."""
    groups: dict[str, list[str]] = {}
    for shot in shots:
        groups.setdefault(shot.fingerprint(), []).append(shot.id)
    return {fp: ids for fp, ids in groups.items() if len(ids) > 1}
