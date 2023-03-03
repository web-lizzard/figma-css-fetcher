from fetchdata import fetch_data
from fetcher import Fetcher


class Converter:
    def __init__(self, fetcher: Fetcher) -> None:
        self.fetcher = fetcher

    def create_font_weights_vars(self) -> None:
        self.fw = [
            f"--font-weight-{w}: {w}; \n" for w in sorted(self.fetcher.font_weights)
        ]

    def create_font_families_vars(self) -> None:
        self.ff = [
            f"--font-{f.replace(' ', '-').lower()}: '{f}'; \n"
            for f in self.fetcher.font_families
        ]

    def create_letter_spacing_vars(self) -> None:
        self.ls = [
            f"--letter-spacing-{set_variables_name_by_index(index)}: {f}px; \n"
            for index, f in enumerate(sorted(self.fetcher.letter_spacing))
        ]

    def create_font_sizes_vars(self) -> None:
        self.fs = [
            f"--fs-{set_variables_name_by_index(index)}: {round((fs / 16), 3)}rem; \n"
            for index, fs in enumerate(sorted(self.fetcher.font_sizes))
        ]

    def create_colors(self):
        self.colors: list[str] = []
        for color in sorted(self.fetcher.colors_set, key=lambda c: c.name):
            color_name = f"--clr-{color.name.replace('_', '-').lower()}"
            value = f": rgba{color.hue}  \n"

            print(value)

            def check(string, color_name):
                if color_name in string:
                    return True

                return False

            color_with_same_name = list(
                filter(lambda x: check(x, color_name=color_name), self.colors)
            )

            if len(color_with_same_name):
                color_index = "".join(char for char in color_name if char.isdigit())

                color_name = color_name.replace(
                    str(color_index),
                    str(int(color_index) + len(color_with_same_name) * 100),
                )

            self.colors.append(color_name + value)

    def convert_values(self) -> None:
        self.fetcher.fetch_values_from_figma(fetch_data())
        self.create_font_families_vars()
        self.create_font_sizes_vars()
        self.create_font_weights_vars()
        self.create_letter_spacing_vars()
        self.create_colors()


def set_variables_name_by_index(index: int):
    return (index + 1) * 100
