import pytest

from converter import Converter
from fetcher import Color


class FetcherMock:
    def __init__(self) -> None:
        self.font_families: set[str] = set()
        self.font_weights: set[str] = set()
        self.font_sizes: set[int] = set()
        self.letter_spacing: set[str] = set()
        self.colors_set: set[Color] = set()

        self.colors_set.add(Color((0, 0, 0, 0), "black"))
        self.font_families.add("Roboto")
        self.font_sizes.add(16)
        self.letter_spacing.add("10")
        self.font_weights.add("500")


def test_init():
    converter = Converter(fetcher=FetcherMock())
