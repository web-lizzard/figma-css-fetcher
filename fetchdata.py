import os

import dotenv
import requests


def fetch_data():
    dotenv.load_dotenv()

    base_url = f"https://api.figma.com/v1/files/{os.environ.get('FIGMA_FILE_NAME')}/"
    headers = {"X-Figma-Token": os.environ.get("FIGMA_API_KEY")}
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as error:
        print(error)
    else:
        data = response.json()
        children = data["document"]["children"]
        return children


def fetch_reset():
    response = requests.get("https://unpkg.com/modern-css-reset/dist/reset.css")
    return response.text
