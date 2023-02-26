from io import TextIOWrapper
from scraper import Scraper


class FileBuilder:
    def __init__(self, scraper: Scraper):
        self.scraper = scraper

        self.blue_clr = self.create_colors_variables(
            colors=self.scraper.blue_colors, color_name="blue"
        )

        self.green_clr = self.create_colors_variables(
            colors=self.scraper.green_colors, color_name="green"
        )

        self.red_clr = self.create_colors_variables(
            colors=self.scraper.red_colors, color_name="red"
        )

        self.gray_clr = self.create_colors_variables(
            colors=self.scraper.gray_colors, color_name="gray"
        )

        self.fw = [
            f"--font-weight-{w}: {w}; \n" for w in sorted(self.scraper.font_weights)
        ]
        self.ff = [f"--font-{f.lower()}: '{f}'; \n" for f in self.scraper.font_families]
        self.ls = [
            f"--letter-spacing-{self.set_variables_name_by_index(index)}: {f}px; \n"
            for index, f in enumerate(sorted(self.scraper.letter_spacing))
        ]
        self.fs = [
            f"--fs-{self.set_variables_name_by_index(index)}: {fs}px; \n"
            for index, fs in enumerate(sorted(self.scraper.font_sizes))
        ]

        self.build_file()

    def build_file(self):
        with open("root.scss", mode="w") as file:
            self.write_file(file)

    def create_colors_variables(self, colors: list, color_name: str):
        return [
            f"--clr-{color_name}-{self.set_variables_name_by_index(index)}: rgba({round(clr.get('r'))}, {round(clr.get('g'))}, {round(clr.get('b'))}, {round(clr.get('a'))}); \n"
            for index, clr in enumerate(
                sorted(
                    colors,
                    key=lambda color: sum(color.values()),
                    reverse=True,
                )
            )
        ]

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
        file.write("//Blue \n")
        file.writelines(self.blue_clr)
        file.write("\n")
        file.write("//Gray \n")
        file.writelines(self.gray_clr)
        file.write("\n")
        file.write("//Red \n")
        file.writelines(self.red_clr)
        file.write("\n")
        file.write("//Green \n")
        file.writelines(self.green_clr)
        file.write("\n")
        file.writelines(self.ls)

        file.write("}")

        return
