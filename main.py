import requests
from webcolors import CSS3_HEX_TO_NAMES
import dotenv
import os

dotenv.load_dotenv()


base_url = f"https://api.figma.com/v1/files/{os.environ.get('FIGMA_FILE_NAME')}/"


headers = {"X-Figma-Token": os.environ.get("FIGMA_API_KEY")}

font_families = set()
font_weights = set()
letter_spacing = set()
colors_set = []
shadows = []


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
    font_families.add(fonts["fontFamily"])
    font_weights.add(fonts["fontWeight"])
    letter_spacing.add(round(fonts["letterSpacing"], 2))


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


# https://api.figma.com/v1/files/w4PzT8VxwxmeBsUzZgqxsO/nodes?ids=1825:3149&depth=1


try:
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()
except requests.HTTPError as error:
    print(error)
else:
    data = response.json()
    children = data["document"]["children"]
    set_properties(children)


with open("root.scss", mode="w") as file:
    fw = [f"--font-weight-{w}: {w}; \n" for w in sorted(font_weights)]
    ff = [f"--font-{f.lower()}: '{f}'; \n" for f in font_families]
    ls = [
        f"--letter-spacing-{(index + 1) * 10}: {f}px; \n"
        for index, f in enumerate(sorted(letter_spacing))
    ]
    file.write(":root { \n")
    file.write("\n")
    file.write("// Font Weights \n")
    file.write("\n")
    file.writelines(fw)
    file.write("\n")
    file.write("// Font Families \n\n")
    file.write("\n")
    file.writelines(ff)
    file.write("\n")
    file.write("//Letters spacings\n")
    file.write("\n")
    file.writelines(ls)

    file.write("}")
