import unittest

from abstracts.abstracts import Fetcher
from converter import Converter
from fetcher import Color


class FetcherMock(Fetcher):
    def __init__(self) -> None:
        self.font_families: set[str] = set()
        self.font_weights: set[str] = set()
        self.font_sizes: set[int] = set()
        self.letter_spacing: set[str] = set()
        self.colors_set: set[Color] = set()

        self.colors_set.add(Color((0, 0, 0, 0), "black"))
        self.font_families.add("Roboto Condensed")
        self.font_sizes.add(16)
        self.font_sizes.add(12)
        self.letter_spacing.add("10")
        self.letter_spacing.add("20")
        self.font_weights.add("500")

    def fetch_values(self, data):
        pass


class Convert_Test_Case(unittest.TestCase):
    def test_init(self):
        fetcher = FetcherMock()
        converter = Converter(fetcher)
        self.assertEqual(converter.fetcher, fetcher)

    def test_create_font_weights_vars(self):
        converter = Converter(FetcherMock())
        converter.create_font_weights_vars()
        self.assertCountEqual(converter.fw, ["--font-weight-500: 500; \n"])

    def test_create_font_families_vars(self):
        converter = Converter(FetcherMock())
        converter.create_font_families_vars()
        self.assertCountEqual(
            converter.ff, ["--font-roboto-condensed: 'Roboto Condensed'; \n"]
        )

    def test_create_letter_spacing_vars(self):
        converter = Converter(FetcherMock())
        converter.create_letter_spacing_vars()
        self.assertCountEqual(
            converter.ls,
            ["--letter-spacing-100: 10px; \n", "--letter-spacing-200: 20px; \n"],
        )

    def test_create_font_sizes_vars(self):
        converter = Converter(FetcherMock())
        converter.create_font_sizes_vars()
        self.assertCountEqual(
            converter.fs, ["--fs-100: 0.75rem; \n", "--fs-200: 1.0rem; \n"]
        )

    def test_create_colors(self):
        converter = Converter(FetcherMock())
        converter.create_colors()
        self.assertEqual(converter.colors, ["--clr-black: rgba(0, 0, 0, 0)  \n"])
