"""User interface modules."""
from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = ["Display", "MockDisplay", "InputHandler", "MockInputHandler"]

_EXPORTS: dict[str, tuple[str, str]] = {
    "Display": (".display", "Display"),
    "MockDisplay": (".display", "MockDisplay"),
    "InputHandler": (".input_handler", "InputHandler"),
    "MockInputHandler": (".input_handler", "MockInputHandler"),
}


def __getattr__(name: str) -> Any:
    """Resolve UI exports lazily."""
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Expose lazy exports to introspection tools."""
    return sorted(list(globals().keys()) + __all__)
