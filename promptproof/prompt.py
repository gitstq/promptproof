"""Turn a structured Shot into a ready-to-paste generation prompt."""
from __future__ import annotations

from .models import Shot


def compose_prompt(shot: Shot) -> str:
    """Compose a labelled prompt so a generator (and a human reviewer)
    can see exactly which part describes subject, action and camera.

    Example output:
        [Subject] an orange cat at a desk
        [Action] turns its head and blinks slowly
        [Camera] slow push-in, medium shot
        [Style] warm natural light, cinematic
    """
    lines = [
        f"[Subject] {shot.subject.strip()}",
        f"[Action] {shot.action.strip()}",
        f"[Camera] {shot.camera.strip()}",
    ]
    if shot.style.strip():
        lines.append(f"[Style] {shot.style.strip()}")
    if shot.source_image.strip():
        lines.append(f"[First frame] {shot.source_image.strip()}")
    if shot.negative.strip():
        lines.append(f"[Avoid] {shot.negative.strip()}")
    return "\n".join(lines)
