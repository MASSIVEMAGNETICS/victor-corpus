"""Bounded connector registry for Victor Corpus organs."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


class OrganRegistrationError(ValueError):
    """Raised when an organ registration would violate registry invariants."""


@dataclass(slots=True)
class OrganConnector:
    """Register and invoke explicitly allowed local organ callables."""

    _organs: dict[str, Callable[..., Any]] = field(default_factory=dict)

    def register(self, name: str, organ: Callable[..., Any]) -> None:
        normalized = name.strip() if isinstance(name, str) else ""
        if not normalized:
            raise OrganRegistrationError("organ name must be a non-empty string")
        if not callable(organ):
            raise TypeError("organ must be callable")
        if normalized in self._organs:
            raise OrganRegistrationError(f"organ already registered: {normalized}")
        self._organs[normalized] = organ

    def invoke(self, name: str, *args: Any, **kwargs: Any) -> Any:
        try:
            organ = self._organs[name]
        except KeyError as exc:
            raise KeyError(f"unknown organ: {name}") from exc
        return organ(*args, **kwargs)

    @property
    def registered_organs(self) -> tuple[str, ...]:
        return tuple(sorted(self._organs))
