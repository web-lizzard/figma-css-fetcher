from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    hue: tuple[int, int, int, int]
    name: str
