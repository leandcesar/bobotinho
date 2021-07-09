# -*- coding: utf-8 -*-
import root  # NOQA
import os
import requests
from requests import Response
from tqdm import tqdm

USERS = []
PATH = "../bobotinho-site/website/static/img/sponsors"
FORMAT = "JP2"


def get_image_url(name: str) -> str:
    url: str = f"http://decapi.me/twitch/avatar/{name}"
    response: Response = requests.get(url)
    response.raise_for_status()
    if response.text.startswith("https://"):
        return response.text
    raise Exception(response.text)


def get_image(url: str) -> Response:
    response: Response = requests.get(url, stream=True)
    response.raise_for_status()
    return response


def download_image(image: Response, path: str, name: str) -> None:
    filename: str = os.path.abspath(os.path.join(path, name))
    with open(filename, "wb") as file:
        for block in image.iter_content(1024):
            if not block:
                break
            file.write(block)


def main() -> None:
    users: list = USERS
    with tqdm(total=len(users)) as progress_bar:
        for name in users:
            name: str = name.lower()
            try:
                url: str = get_image_url(name)
                image: str = get_image(url)
            except Exception as e:
                print(f"Invalid response for user with name \"{name}\": {e}")
                continue
            else:
                download_image(image, PATH, f"{name}.{FORMAT}")
            progress_bar.update(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
