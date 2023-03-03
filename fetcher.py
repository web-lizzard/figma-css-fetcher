from dataclasses import dataclass

from webcolors import hex_to_rgb

from color_palette import names_to_hex


def convert_rgb_to_names(rgb: tuple) -> str:
    differences = {}
    for color_name, color_hex in names_to_hex.items():
        r, g, b = hex_to_rgb(color_hex)
        differences[
            sum([(r - rgb[0]) ** 2, (g - rgb[1]) ** 2, (b - rgb[2]) ** 2])
        ] = color_name
    return differences[min(differences.keys())]


@dataclass(frozen=True)
class Color:
    hue: tuple[int, int, int, int]
    name: str


class Fetcher:
    def __init__(self):
        self.font_families: set[str] = set()
        self.font_weights: set[str] = set()
        self.font_sizes: set[int] = set()
        self.letter_spacing: set[str] = set()
        self.colors_set: set[Color] = set()
        self.shadows = []

    def fetch_values_from_figma(self, children):

        for child in children:

            colors = child.get("backgroundColor")
            font_style = child.get("style")
            effects = child.get("effects")

            if colors:
                self.set_colors(colors)

            if font_style:
                self.set_fonts(font_style)

            if effects:
                self.set_shadows(effects)

            nodes = child.get("children")

            if nodes and len(nodes):
                self.fetch_values_from_figma(nodes)

    def set_colors(self, colors):
        color_tuple = tuple((round(hue * 255)) for hue in colors.values())

        color = Color(hue=color_tuple, name=convert_rgb_to_names(color_tuple))

        self.colors_set.add(color)

    def set_fonts(self, fonts):
        self.font_families.add(fonts["fontFamily"])
        self.font_weights.add(fonts["fontWeight"])
        self.letter_spacing.add(round(fonts["letterSpacing"], 2))
        self.font_sizes.add(round(fonts["fontSize"]))

    def set_shadows(self, effects):
        for effect in effects:
            pass
