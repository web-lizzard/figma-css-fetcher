from fetch_data import fetch_data


class Scraper:
    def __init__(self):
        self.font_families = set()
        self.font_weights = set()
        self.font_sizes = set()
        self.letter_spacing = set()
        self.colors_set = []
        self.shadows = []

        self.blue_colors = []
        self.red_colors = []
        self.green_colors = []
        self.gray_colors = []

        self.scrap_values_from_figma(fetch_data())
        self.create_colors_list()

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
        color = {hue: colors[hue] * 255 for hue in colors}
        if not color in self.colors_set:
            self.colors_set.append(color)

    def set_fonts(self, fonts):
        self.font_families.add(fonts["fontFamily"])
        self.font_weights.add(fonts["fontWeight"])
        self.letter_spacing.add(round(fonts["letterSpacing"], 2))
        self.font_sizes.add(round(fonts["fontSize"]))

    def set_shadows(self, effects):
        for effect in effects:
            pass

    def create_colors_list(self):
        for color in self.colors_set:
            dict_without_alpha = color.copy()
            dict_without_alpha.pop("a")
            dominated_hue = max(dict_without_alpha, key=dict_without_alpha.get)

            if dominated_hue == "g":
                if abs(color[dominated_hue] - color.get("b")) <= 40 and abs(
                    color[dominated_hue] - color.get("r") <= 40
                    and color[dominated_hue] != 255
                ):
                    self.gray_colors.append(color)
                else:
                    self.green_colors.append(color)
            elif dominated_hue == "b":
                if abs(color[dominated_hue] - color.get("g")) <= 40 and abs(
                    color[dominated_hue] - color.get("r") <= 40
                    and color[dominated_hue] != 255
                ):
                    self.gray_colors.append(color)
                else:
                    self.blue_colors.append(color)
            else:
                if abs(color[dominated_hue] - color.get("g")) <= 40 and abs(
                    color[dominated_hue] - color.get("b") <= 40
                    and color[dominated_hue] != 255
                ):
                    self.gray_colors.append(color)
                else:
                    self.red_colors.append(color)
