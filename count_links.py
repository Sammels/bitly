import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

API = "https://api-ssl.bitly.com/v4/"


def shorten_link(token: str, url: str) -> str:
    """Function get token and default url, them return short url"""
    url_link = f"{API}shorten"
    header = {"Authorization": f"Bearer {token}"}
    payload = {"long_url": url}
    url_response = requests.post(url_link, headers=header, json=payload)
    url_response.raise_for_status()
    short_link = url_response.json()
    bitlink = short_link['link']
    return bitlink


def count_clics(token: str, link: str):
    """Function get token, short link -> return count clics"""
    netloc, url_path = urlparse(link).netloc, urlparse(link).path
    link = f"{netloc}{url_path}"
    url_link = f"{API}bitlinks/{link}/clicks/summary"
    header = {"Authorization": f"Bearer {token}"}
    payload = {"unit": "day",
               "units": -1}
    response = requests.get(url_link, headers=header, params=payload)
    clics = response.json()
    clics = clics['total_clicks']
    return clics


def is_bitlink(token: str, url: str) -> bool:
    """Check link. bitlink or not"""
    netloc, url_path = urlparse(url).netloc, urlparse(url).path
    url = f"{netloc}{url_path}"
    url_link = f"{API}bitlinks/{url}"
    header = {"Authorization": f"Bearer {token}"}
    response = requests.get(url_link, headers=header)
    return response.ok


def main():
    load_dotenv()
    token = os.environ["BITLINK_TOKEN"]
    input_url = input("Введите ссылку: ")
    resp = is_bitlink(token, input_url)
    if resp:
        click_count = count_clics(token, input_url)
        print(f"По вашей ссылке прошли {click_count} раз(а)")
    else:
        bitlink = shorten_link(token, input_url)
        print(f"Битлинк: {bitlink}")


if __name__ == "__main__":
    main()
