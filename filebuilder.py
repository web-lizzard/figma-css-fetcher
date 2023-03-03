import os
from io import TextIOWrapper

from converter import Converter
from fetchdata import fetch_data, fetch_reset
from fetcher import Fetcher


class FileBuilder:
    def __init__(self, converter: Converter):
        self.converter = converter

        try:
            os.mkdir("scss")
        except FileExistsError:
            pass

    def build_root_file(self):
        with open("scss/root.scss", mode="w") as file:
            file.write('@forward "reset";\n\n')
            self.write_file(file)

    def build_utilities(self):
        with open("scss/utilities.scss", mode="w") as file:
            text_colors = []
            background_colors = []
            font_sizes = []

            for color in self.converter.colors:
                text_color = self.create_colors_utilities(color, "clr", "text", "color")
                background_color = self.create_colors_utilities(
                    color, "clr", "bg", "background-color"
                )
                text_colors.append(text_color)
                background_colors.append(background_color)

            for font in self.converter.fs:
                font = self.create_colors_utilities(font, "fs", "fs", "font-size")
                font_sizes.append(font)

            file.write("@forward 'root'; \n\n")
            file.writelines(text_colors)
            file.writelines(background_colors)
            file.writelines(font_sizes)

            file.write(".grid {\n  display: grid; \n  gap: var(--space, 1rem);\n}\n\n")
            file.write(".flex {\n  display: flex; \n  gap: var(--space, 1rem);\n}\n\n")
            file.write(
                ":where(.flow > * + *) {\n  margin-top: var(--space, 1rem);\n}\n\n"
            )

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
        file.writelines(self.converter.fw)
        file.write("\n")
        file.write("// Font Families \n\n")
        file.writelines(self.converter.ff)
        file.write("\n")
        file.write("// Font Sizes \n\n")
        file.writelines(self.converter.fs)
        file.write("\n")
        file.write("//Colors \n")
        file.writelines(self.converter.colors)
        file.write("\n")
        file.writelines(self.converter.ls)

        file.write("}")

    def create_colors_utilities(
        self, color: str, css_prefix: str, prefix: str, property: str
    ):
        css_variable = color.split(":")[0]
        class_name = css_variable.split(f"--{css_prefix}-")[1]
        class_content = (
            f".{prefix}-{class_name} {{\n   {property}: var({css_variable}); \n}}\n\n"
        )
        return class_content
