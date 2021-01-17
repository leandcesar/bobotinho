# -*- coding: utf-8 -*-

"""
bobotinho - Twitch bot for Brazilian offstream chat entertainment
Copyright (C) 2020  Leandro César

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Adapted from: https://github.com/felipemfp/dicio

import html
import re

from unidecode import unidecode
from utils import asyncrq

BASE_URL = "http://www.dicio.com.br/{}/"
TAG_MEANING = ('class="significado', "</p>")
TAG_ETYMOLOGY = ('class="etim', "</span>")
TAG_SYNONYMS = ('class="adicional sinonimos"', "</p>")
TAG_SYNONYMS_DELIMITER = ("<a", "</a>")
TAG_EXTRA = ('class="adicional"', "</p>")
TAG_EXTRA_SEP = "br"
TAG_EXTRA_DELIMITER = ("<b>", "</b>")
TAG_PHRASE_DELIMITER = ('<div class="frase"', "</div>")


class Utils(object):
    @staticmethod
    def text_between(text: str, before: str, after: str) -> str:
        """Retorna o texto entre duas palavras."""
        start = text.find(before)
        if start != -1:
            start += len(before)
        if before[-1] != ">":
            start = text.find(">", start) + 1
        end = text.find(after, start)
        if after[0] != "<":
            end = text.find("<", start)
        if -1 < start < end:
            return text[start:end]
        return text.strip().lower()

    @staticmethod
    def remove_accents(text: str) -> str:
        """Remove acentos."""
        return unidecode(text)

    @staticmethod
    def remove_spaces(text: str) -> str:
        """Substitui múltiplos espaços, tabulações e outros."""
        return re.sub("[\t\n\r ]+", " ", text).strip()

    @staticmethod
    def remove_tags(html: str) -> str:
        """Remove tags html."""
        return re.sub("<[^>]*>", " ", html).strip()

    @staticmethod
    def split_html_tag(text: str, tag: str) -> list:
        """Divide o texto nas tags html."""
        return list(filter(None, re.split("<[^>]*{0}[^>]*>".format(tag), text)))


class Word(object):
    def __init__(self, word, meaning=None, etymology=None, synonyms=[], examples=[], extra={}):
        self.word = word.strip().lower()
        self.url = BASE_URL.format(Utils.remove_accents(self.word))
        self.meaning = meaning
        self.etymology = etymology
        self.synonyms = synonyms
        self.extra = extra
        self.examples = examples


class Dicio:
    async def _request(self, word: str) -> str:
        """[Interno] Obtém a página html da palavra."""
        try:
            word = Utils.remove_accents(word).strip().lower()
            response = await asyncrq.get(BASE_URL.format(word), res_method="text")
            return html.unescape(response)
        except:
            return None

    def _scrape_meaning(self, page: str) -> (str, str):
        """[Interno] Obtém o significado e etimologia da palavra."""
        html = Utils.text_between(page, *TAG_MEANING)
        etymology = Utils.text_between(html, *TAG_ETYMOLOGY)
        etymology = Utils.remove_tags(etymology)
        etymology = Utils.remove_spaces(etymology)
        meanings = Utils.split_html_tag(html, "br")
        meanings = [Utils.remove_spaces(Utils.remove_tags(x)) for x in meanings]
        meanings = "; ".join([x for x in meanings if x != etymology])
        return (meanings, etymology)

    def _first_synonym(self, html: str) -> (Word, str):
        """[Interno] Obtém o primeiro sinônimo da palavra."""
        synonym = Utils.text_between(html, *TAG_SYNONYMS_DELIMITER)
        synonym = Utils.remove_spaces(synonym)
        html = html.replace(TAG_SYNONYMS_DELIMITER[0], "", 1)
        html = html.replace(TAG_SYNONYMS_DELIMITER[1], "", 1)
        return (Word(synonym), html)

    def _scrape_synonyms(self, page: str) -> str:
        """[Interno] Obtém os sinônimos da palavra."""
        synonyms = []
        if page.find(TAG_SYNONYMS[0]) != -1:
            html = Utils.text_between(page, *TAG_SYNONYMS)
            while html.find(TAG_SYNONYMS_DELIMITER[0]) != -1:
                synonym, html = self._first_synonym(html)
                synonyms.append(synonym)
        return synonyms

    def _scrape_examples(self, page: str) -> str:
        """[Interno] Obtém os exemplos da palavra."""
        examples = []
        index = page.find(TAG_PHRASE_DELIMITER[0])
        while index != -1:
            example_html = Utils.text_between(page, *TAG_PHRASE_DELIMITER)
            examples += [Utils.remove_spaces(Utils.remove_tags(example_html))]
            page = page[index + len(TAG_PHRASE_DELIMITER[0]) :]
            index = page.find(TAG_PHRASE_DELIMITER[0])
        return examples

    def _scrape_extra(self, page: str) -> dict:
        """[Interno] Obtém informações extras da palavra."""
        dict_extra = {}
        if page.find(TAG_EXTRA[0]) != -1:
            try:
                html = Utils.text_between(page, *TAG_EXTRA)
                extra_rows = Utils.split_html_tag(Utils.remove_spaces(html), TAG_EXTRA_SEP)
                for row in extra_rows:
                    key, value = Utils.remove_spaces(Utils.remove_tags(row)).split(":")
                    dict_extra[key] = value
            except:
                pass
        return dict_extra

    async def exists(self, word: str) -> bool:
        """Verifica se a palavra existe."""
        word = word.lower()
        page = await self._request(word)
        title = Utils.text_between(page, "<h1", "</h1>")
        return unidecode(title) == unidecode(word)
    
    async def search(self, word: str) -> Word:
        """Retorna um objeto Word da palavra."""
        word = word.lower()
        page = await self._request(word)
        meaning, etymology = self._scrape_meaning(page)
        return Word(
            Utils.text_between(page, "<h1", "</h1>"),
            meaning=meaning,
            etymology=etymology,
            synonyms=self._scrape_synonyms(page),
            examples=self._scrape_examples(page),
            extra=self._scrape_extra(page),
        )

    async def meaning(self, word: str) -> str:
        """Retorna o significado da palavra."""
        word = word.lower()
        page = await self._request(word)
        meaning, _ = self._scrape_meaning(page)
        return meaning

    async def synonyms(self, word: str) -> str:
        """Retorna o sinônimo da palavra."""
        word = word.lower()
        page = await self._request(word)
        synonyms = self._scrape_synonyms(page)
        return synonyms
