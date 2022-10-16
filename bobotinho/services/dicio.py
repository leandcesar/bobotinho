# -*- coding: utf-8 -*-
import html
import re
from aiohttp import ClientSession

__all__ = ("Dicio",)


class Utils:

    @staticmethod
    def remove_tags(html: str) -> str:
        new_text = ""
        tag = False
        for char in html:
            if not tag and char == "<":
                tag = True
            elif not tag:
                new_text += char
            elif tag and char == ">":
                tag = False
        return new_text

    @staticmethod
    def text_between(text: str, before: str, after: str) -> str:
        start = text.find(before)
        if start > -1:
            start += len(before)
        if before[-1] != ">":
            start = text.find(">", start) + 1
        end = text.find(after, start)
        if after[0] != "<":
            end = text.find("<", start)
        if -1 < start < end:
            return text[start:end]
        return ""

    @staticmethod
    def remove_spaces(text: str) -> str:
        text = text.replace("\t", " ")
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        while text.find("  ") > -1:
            text = text.replace("  ", " ")
        return text.strip()

    @staticmethod
    def remove_accents(text: str) -> str:
        reference = [('a', 'áàâãä'), ('e', 'éèêë'), ('i', 'íìîï'), ('o', 'óòôõö'), ('u', 'úùûü'), ('c', 'ç')]
        new_text = ""
        for char in text:
            for clear_vowal, possible_accents in reference:
                if char in possible_accents:
                    new_text += clear_vowal
                    break
            else:
                new_text += char
        return new_text

    @staticmethod
    def split_html_tag(text: str, tag: str) -> str:
        return list(filter(None, re.split(f'<[^>]*{tag}[^>]*>', text)))


class Word:

    def __init__(self, page: str) -> None:
        self.page = page
        self.label = Utils.text_between(self.page, "<h1", "</h1>")

    def __str__(self) -> str:
        return self.label

    def __bool__(self) -> bool:
        return self.label != "Não encontrada"

    def meaning(self) -> str:
        html = Utils.text_between(page, 'class="significado', '</p>')
        meaning = Utils.split_html_tag(html, 'span')
        meaning = [Utils.remove_spaces(Utils.remove_tags(x)) for x in meaning]
        meaning = " ".join([x for x in meaning if x and x != etymology]).replace(word_class, "").replace(etymology, "")
        return meaning

    def etymology(self) -> str:
        html = Utils.text_between(page, 'class="significado', '</p>')
        etymology = Utils.text_between(html, 'class="etim', '</span>')
        etymology = Utils.remove_spaces(Utils.remove_tags(etymology))
        return etymology

    def word_class(self) -> str:
        html = Utils.text_between(page, 'class="significado', '</p>')
        word_class = Utils.text_between(html, 'class="cl', '</span>')
        word_class = Utils.remove_spaces(Utils.remove_tags(word_class))
        return word_class

    def synonyms(self) -> str:
        synonyms = []
        if page.find('class="adicional sinonimos"') > -1:
            html = Utils.text_between(page, 'class="adicional sinonimos"', '</p>')
            while html.find('<a') > -1:
                synonym = Utils.text_between(html, '<a', '</a>')
                synonym = Utils.remove_spaces(synonym).strip().lower()
                synonyms.append(synonym)
                html = html.replace('<a', "", 1).replace('</a>', "", 1)
        return ", ".join(synonyms)


class Dicio:
    def __init__(self, *, session: ClientSession = None) -> None:
        self.session = session or ClientSession(raise_for_status=False)

    async def close(self) -> None:
        await self.session.close()

    async def exists(self, *, query: str) -> bool:
        query = Utils.remove_accents(query).lower()
        async with self.session.get(url=f"http://www.dicio.com.br/{query}") as response:
            data = await response.text()
            page = html.unescape(data)
            return bool(Word(page))
