import requests
from webcolors import CSS3_HEX_TO_NAMES


base_url = "https://api.figma.com/v1/files/w4PzT8VxwxmeBsUzZgqxsO/"

api_key = "figd_zomKpO19BWGLMBuhe08C8QBdIf34yfdiFW2XJSQZ"

params = {"depth": 1}

headers = {"X-Figma-Token": api_key}

font_families = set()
font_weights = set()
letter_spacing = set()
colors_set = []
shadows = []
# https://api.figma.com/v1/files/w4PzT8VxwxmeBsUzZgqxsO/nodes?ids=1825:3149&depth=1


def set_shadows(effects):
    for effect in effects:
        print(effect)


def set_colors(colors):
    global colors_set
    color = [colors[hue] * 255 for hue in colors]
    if not color is colors_set:
        colors_set.append(color)


def set_fonts(fonts):
    global font_families
    global font_weights
    font_families.add(fonts["fontFamily"])
    font_weights.add(fonts["fontWeight"])
    letter_spacing.add(fonts["letterSpacing"])


def set_properties(children):
    global colors_set
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
