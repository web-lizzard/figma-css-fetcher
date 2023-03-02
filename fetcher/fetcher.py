from fetcher.fetchdata import fetch_data
from webcolors import (
    hex_to_rgb,
)
from fetcher.color_palette import names_to_hex


def convert_rgb_to_names(rgb: tuple) -> str:
    differences = {}
    for color_name, color_hex in names_to_hex.items():
        r, g, b = hex_to_rgb(color_hex)
        differences[
            sum([(r - rgb[0]) ** 2, (g - rgb[1]) ** 2, (b - rgb[2]) ** 2])
        ] = color_name
    return differences[min(differences.keys())]


class Fetcher:
    def __init__(self):
        self.font_families = set()
        self.font_weights = set()
        self.font_sizes = set()
        self.letter_spacing = set()
        self.colors_set = set()
        self.shadows = []
        self.colors = []

        self.scrap_values_from_figma(fetch_data())
        for color in self.colors_set:
            self.append_new_color(color)

    def scrap_values_from_figma(self, children):

        for child in children:
            nodes = child.get("children")

            colors = child.get("backgroundColor")
            type_style = child.get("style")
            effects = child.get("effects")

            if colors:
                self.set_colors(colors)

            if type_style:
                self.set_fonts(type_style)

            if effects:
                self.set_shadows(effects)

            if nodes and len(nodes):
                self.scrap_values_from_figma(nodes)

    def set_colors(self, colors):
        color = tuple((round(colors[hue] * 255)) for hue in colors)
        self.colors_set.add(color)

    def set_fonts(self, fonts):
        self.font_families.add(fonts["fontFamily"])
        self.font_weights.add(fonts["fontWeight"])
        self.letter_spacing.add(round(fonts["letterSpacing"], 2))
        self.font_sizes.add(round(fonts["fontSize"]))

    def set_shadows(self, effects):
        for effect in effects:
            pass

    def append_new_color(self, color: dict):
        self.colors.append(
            {
                "name": convert_rgb_to_names((color[0], color[1], color[2])),
                "color": color,
            }
        )
