import requests
import dotenv
import os
import gc

from scraper import Scraper


dotenv.load_dotenv()

base_url = f"https://api.figma.com/v1/files/{os.environ.get('FIGMA_FILE_NAME')}/"

headers = {"X-Figma-Token": os.environ.get("FIGMA_API_KEY")}

# font_families = set()
# font_weights = set()
# font_sizes = set()
# letter_spacing = set()
# colors_set = []
# shadows = []

# blue_colors = []
# red_colors = []
# green_colors = []
# gray_colors = []


def fetch_data():
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as error:
        print(error)
    else:
        return response.json()


def main():
    data = fetch_data()
    children = data["document"]["children"]
    set_properties(children)


def create_colors_list(colors_set):
    for color in colors_set:
        dict_without_alpha = color.copy()
        dict_without_alpha.pop("a")
        dominated_hue = max(dict_without_alpha, key=dict_without_alpha.get)

        if dominated_hue == "g":
            if abs(color[dominated_hue] - color.get("b")) <= 40 and abs(
                color[dominated_hue] - color.get("r") <= 40
                and color[dominated_hue] != 255
            ):
                gray_colors.append(color)
            else:
                green_colors.append(color)
        elif dominated_hue == "b":
            if abs(color[dominated_hue] - color.get("g")) <= 40 and abs(
                color[dominated_hue] - color.get("r") <= 40
                and color[dominated_hue] != 255
            ):
                gray_colors.append(color)
            else:
                blue_colors.append(color)
        else:
            if abs(color[dominated_hue] - color.get("g")) <= 40 and abs(
                color[dominated_hue] - color.get("b") <= 40
                and color[dominated_hue] != 255
            ):
                gray_colors.append(color)
            else:
                red_colors.append(color)

    # check if color hue is the biggest from dict (r, g, b), save color to one of list (reds_colors, green_colors, blues_colors), create separate clr css variables and append to root


def set_shadows(effects):
    for effect in effects:
        pass


def set_colors(colors):
    global colors_set
    color = {hue: colors[hue] * 255 for hue in colors}
    if not color in colors_set:
        colors_set.append(color)


def set_fonts(fonts):
    global font_families
    global font_weights
    global font_sizes
    font_families.add(fonts["fontFamily"])
    font_weights.add(fonts["fontWeight"])
    letter_spacing.add(round(fonts["letterSpacing"], 2))
    font_sizes.add(round(fonts["fontSize"]))


def set_properties(children):
    for child in children:
        nodes = child.get("children")

        colors = child.get("backgroundColor")
        type_style = child.get("style")
        effects = child.get("effects")

        if colors:
            set_colors(colors)

        if type_style:
            set_fonts(type_style)

        if effects:
            set_shadows(effects)

        if nodes and len(nodes):
            set_properties(nodes)


def create_scss_file():
    scraper = Scraper()
    with open("root.scss", mode="w") as file:

        blue_clr = [
            f"--clr-blue-{(index + 1) * 100}: rgba({round(clr.get('r'))}, {round(clr.get('g'))}, {round(clr.get('b'))}, {round(clr.get('a'))}); \n"
            for index, clr in enumerate(
                sorted(
                    scraper.blue_colors,
                    key=lambda color: sum(color.values()),
                    reverse=True,
                )
            )
        ]

        green_clr = [
            f"--clr-green-{(index + 1) * 100}: rgba({round(clr.get('r'))}, {round(clr.get('g'))}, {round(clr.get('b'))}, {round(clr.get('a'))}); \n"
            for index, clr in enumerate(
                sorted(
                    scraper.green_colors,
                    key=lambda color: sum(color.values()),
                    reverse=True,
                )
            )
        ]

        red_clr = [
            f"--clr-red-{(index + 1) * 100}: rgba({round(clr.get('r'))}, {round(clr.get('g'))}, {round(clr.get('b'))}, {round(clr.get('a'))}); \n"
            for index, clr in enumerate(
                sorted(
                    scraper.red_colors,
                    key=lambda color: sum(color.values()),
                    reverse=True,
                )
            )
        ]

        gray_clr = [
            f"--clr-gray-{(index + 1) * 100}: rgba({round(clr.get('r'))}, {round(clr.get('g'))}, {round(clr.get('b'))}, {round(clr.get('a'))}); \n"
            for index, clr in enumerate(
                sorted(
                    scraper.gray_colors,
                    key=lambda color: sum(color.values()),
                    reverse=True,
                )
            )
        ]

        fw = [f"--font-weight-{w}: {w}; \n" for w in sorted(scraper.font_weights)]
        ff = [f"--font-{f.lower()}: '{f}'; \n" for f in scraper.font_families]
        ls = [
            f"--letter-spacing-{(index + 1) * 10}: {f}px; \n"
            for index, f in enumerate(sorted(scraper.letter_spacing))
        ]
        fs = [
            f"--fs-{(index + 1) * 100}: {fs}px; \n"
            for index, fs in enumerate(sorted(scraper.font_sizes))
        ]
        file.write(":root { \n")
        file.write("// Font Weights \n")
        file.write("\n")
        file.writelines(fw)
        file.write("\n")
        file.write("// Font Families \n\n")
        file.writelines(ff)
        file.write("\n")
        file.write("// Font Sizes \n\n")
        file.writelines(fs)
        file.write("\n")
        file.write("//Colors \n")
        file.write("//Blue \n")
        file.writelines(blue_clr)
        file.write("\n")
        file.write("//Gray \n")
        file.writelines(gray_clr)
        file.write("\n")
        file.write("//Red \n")
        file.writelines(red_clr)
        file.write("\n")
        file.write("//Green \n")
        file.writelines(green_clr)
        file.write("\n")
        file.writelines(ls)

        file.write("}")


create_scss_file()
gc.collect()
print(len(gc.get_objects()))
