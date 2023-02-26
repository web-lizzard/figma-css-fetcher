from io import TextIOWrapper
import os
from fetcher import Fetcher
from fetchdata import fetch_reset


class FileBuilder:
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher
        self.colors = []
        self.create_colors()

        self.fw = [
            f"--font-weight-{w}: {w}; \n" for w in sorted(self.fetcher.font_weights)
        ]
        self.ff = [
            f"--font-{f.replace(' ', '-').lower()}: '{f}'; \n"
            for f in self.fetcher.font_families
        ]
        self.ls = [
            f"--letter-spacing-{self.set_variables_name_by_index(index)}: {f}px; \n"
            for index, f in enumerate(sorted(self.fetcher.letter_spacing))
        ]
        self.fs = [
            f"--fs-{self.set_variables_name_by_index(index)}: {round((fs / 16), 3)}rem; \n"
            for index, fs in enumerate(sorted(self.fetcher.font_sizes))
        ]

        try:
            os.mkdir("scss")
        except FileExistsError:
            pass

    def build_root_file(self):
        with open("scss/root.scss", mode="w") as file:
            self.write_file(file)

    def build_utilities(self):
        with open("scss/utilities.scss", mode="w") as file:
            text_colors = []
            background_colors = []
            font_sizes = []

            for color in self.colors:
                text_color = self.create_colors_utilities(color, "clr", "text", "color")
                background_color = self.create_colors_utilities(
                    color, "clr", "bg", "background-color"
                )
                text_colors.append(text_color)
                background_colors.append(background_color)

            for font in self.fs:
                font = self.create_colors_utilities(font, "fs", "fs", "font-size")
                font_sizes.append(font)

            file.write("@forward 'root'; \n\n")
            file.writelines(text_colors)
            file.writelines(background_colors)
            file.writelines(font_sizes)

    def set_variables_name_by_index(self, index: int):
        return (index + 1) * 100

    def create_reset_scss(self):
        with open("scss/reset.scss", mode="w") as file:
            content = fetch_reset()
            file.writelines(content)

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

            self.colors.append(color_name + value)

    def create_colors_utilities(
        self, color: str, css_prefix: str, prefix: str, property: str
    ):
        css_variable = color.split(":")[0]
        class_name = css_variable.split(f"--{css_prefix}-")[1]
        class_content = (
            f".{prefix}-{class_name} {{\n   {property}: var({css_variable}); \n}}\n\n"
        )
        return class_content
