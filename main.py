import requests

base_url = "https://api.figma.com/v1/files/w4PzT8VxwxmeBsUzZgqxsO/"

api_key = "figd_zomKpO19BWGLMBuhe08C8QBdIf34yfdiFW2XJSQZ"

params = {"depth": 1}

headers = {"X-Figma-Token": api_key}

colors = set()

# https://api.figma.com/v1/files/w4PzT8VxwxmeBsUzZgqxsO/nodes?ids=1825:3149&depth=1


def set_properties(children):
    for child in children:
        nodes = child.get("children")

        colors = child.get("backgroundColor")
        type_style = child.get("style")
        effects = child.get("effects")

        if colors:
            pass

        if type_style:
            pass

        if effects:
            print(effects)

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
