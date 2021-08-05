# -*- coding: utf-8 -*-
import json
import requests
import urllib3
from urllib.parse import quote
from bobotinho import config

FILENAME = "bobotinho//data//languages.json"

with open(FILENAME, "r", encoding="utf-8") as file:
    LANGUAGES = json.load(file)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Translator:
    timeout = 5
    proxies = {}
    base_url = config.translate_url
    headers = {
        "Referer": "https://translate.google.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/47.0.2526.106 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    @staticmethod
    def _package_rpc(text: str, lang_src: str = "auto", lang_tgt: str = "auto"):
        escaped_parameter = json.dumps([[text.strip(), lang_src, lang_tgt, True], [1]], separators=(",", ":"))
        espaced_rpc = json.dumps([[["MkEWBc", escaped_parameter, None, "generic"]]], separators=(",", ":"))
        return f"f.req={quote(espaced_rpc)}&"

    @classmethod
    def translate(cls, text: str, lang_tgt: str = "auto", lang_src: str = "auto"):
        lang_src = lang_src if LANGUAGES.get(lang_src) else "auto"
        lang_src = lang_src if LANGUAGES.get(lang_tgt) else "auto"
        response = requests.Request(
            method="POST",
            url=cls.base_url,
            data=cls._package_rpc(text, lang_src, lang_tgt),
            headers=cls.headers,
        )
        with requests.Session() as s:
            s.proxies = cls.proxies
            r = s.send(request=response.prepare(), verify=False, timeout=cls.timeout)
        for line in r.iter_lines(chunk_size=1024):
            decoded_line = line.decode("utf-8")
            if "MkEWBc" in decoded_line:
                _response = list(json.loads(list(json.loads(decoded_line))[0][2]))
                response = _response[1][0]
                if len(response) == 1:
                    if len(response[0]) <= 5:
                        translate_text = response[0][0]
                        return translate_text
                    translate_text = ""
                    sentences = response[0][5]
                    for sentence in sentences:
                        translate_text += sentence[0].strip() + " "
                    return translate_text

    @classmethod
    def detect(cls, text: str):
        response = requests.Request(
            method="POST",
            url=cls.base_url,
            data=cls._package_rpc(text),
            headers=cls.headers,
        )
        with requests.Session() as s:
            s.proxies = cls.proxies
            r = s.send(request=response.prepare(), verify=False, timeout=cls.timeout)
        for line in r.iter_lines(chunk_size=1024):
            decoded_line = line.decode("utf-8")
            if "MkEWBc" in decoded_line:
                _response = list(json.loads(list(json.loads(decoded_line))[0][2]))
                return _response[0][2]
