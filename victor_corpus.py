"""Core identity primitive for the Victor Corpus package.

This module intentionally implements only the behavior the repository can
currently verify. It does not claim persistent memory, autonomy, or cognition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256


@dataclass(frozen=True, slots=True)
class VictorCorpus:
    """A minimal, deterministic Victor Corpus identity container.

    Args:
        bloodline_seed: Optional private seed used to derive a non-reversible
            identity fingerprint. The raw seed is not retained.

    Raises:
        TypeError: If bloodline_seed is not a string.
        ValueError: If a supplied seed is blank.
    """

    bloodline_seed: str | None = field(default=None, repr=False, compare=False)
    identity: str = field(init=False)
    bloodline_fingerprint: str | None = field(init=False)

    def __post_init__(self) -> None:
        seed = self.bloodline_seed
        if seed is not None:
            if not isinstance(seed, str):
                raise TypeError("bloodline_seed must be a string or None")
            if not seed.strip():
                raise ValueError("bloodline_seed cannot be blank")

        fingerprint = sha256(seed.encode("utf-8")).hexdigest() if seed else None
        suffix = f" [{fingerprint[:12]}]" if fingerprint else ""

        object.__setattr__(self, "identity", f"Victor Corpus v1.0.0{suffix}")
        object.__setattr__(self, "bloodline_fingerprint", fingerprint)
        object.__setattr__(self, "bloodline_seed", None)
