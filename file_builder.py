from io import TextIOWrapper
from fetcher import Fetcher
import re


class FileBuilder:
    def __init__(self, scraper: Fetcher):
        self.scraper = scraper
        self.colors = []
        self.create_colors()

        self.fw = [
            f"--font-weight-{w}: {w}; \n" for w in sorted(self.scraper.font_weights)
        ]
        self.ff = [
            f"--font-{f.replace(' ', '-').lower()}: '{f}'; \n"
            for f in self.scraper.font_families
        ]
        self.ls = [
            f"--letter-spacing-{self.set_variables_name_by_index(index)}: {f}px; \n"
            for index, f in enumerate(sorted(self.scraper.letter_spacing))
        ]
        self.fs = [
            f"--fs-{self.set_variables_name_by_index(index)}: {round((fs / 16), 3)}rem; \n"
            for index, fs in enumerate(sorted(self.scraper.font_sizes))
        ]

    def build_root_file(self):
        with open("root.scss", mode="w") as file:
            self.write_file(file)

    def set_variables_name_by_index(self, index: int):
        return (index + 1) * 100

    def write_file(self, file: TextIOWrapper):
        file.write(":root { \n")
        file.write("// Font Weights \n")
        file.write("\n")
        file.writelines(self.fw)
        file.write("\n")
        file.write("// Font Families \n\n")
        file.writelines(self.ff)
        file.write("\n")
        file.write("// Font Sizes \n\n")
        file.writelines(self.fs)
        file.write("\n")
        file.write("//Colors \n")
        file.writelines(self.colors)
        file.write("\n")
        file.writelines(self.ls)

        file.write("}")

    def create_colors(self):
        for color in sorted(self.scraper.colors, key=lambda c: c["name"]):
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

            self.colors.append(color_name + value)
