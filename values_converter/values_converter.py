from fetcher.fetcher import Fetcher


class ValuesConverter:
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher

    def create_font_weights_vars(self):
        return [
            f"--font-weight-{w}: {w}; \n" for w in sorted(self.fetcher.font_weights)
        ]

    def create_font_families_var(self):
        return [
            f"--font-{f.replace(' ', '-').lower()}: '{f}'; \n"
            for f in self.fetcher.font_families
        ]

    def create_letters_spacing_var(self):
        return [
            f"--letter-spacing-{self.set_variables_name_by_index(index)}: {f}px; \n"
            for index, f in enumerate(sorted(self.fetcher.letter_spacing))
        ]

    def create_font_sizes_var(self):
        return [
            f"--fs-{self.set_variables_name_by_index(index)}: {round((fs / 16), 3)}rem; \n"
            for index, fs in enumerate(sorted(self.fetcher.font_sizes))
        ]

    def create_colors_vars(self) -> list[str]:
        colors = []

        for color in sorted(self.fetcher.colors, key=lambda c: c["name"]):
            color_name = f"--clr-{color['name'].replace('_', '-').lower()}"
            value = f": rgba({color['color'][0]}, {color['color'][1]}, {color['color'][2]}, {color['color'][3]}); \n"

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

            colors.append(color_name + value)

        return colors

    def set_variables_name_by_index(self, index: int):
        return (index + 1) * 100
