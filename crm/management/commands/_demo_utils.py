"""OCTAX demo record markers. Only marked records are eligible for cleanup."""
import re
from django.core.management.base import CommandError

PREFIX = "[OCTAX-DEMO:"
MARKER_PATTERN = re.compile(r"^\[OCTAX-DEMO:([a-zA-Z0-9_-]{1,40})\]$")

def marker(batch):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,40}", batch):
        raise CommandError("Batch must be 1-40 letters, digits, underscores or hyphens")
    return f"[OCTAX-DEMO:{batch}]"
