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

# Adapted from: https://github.com/felipemfp/dicio/blob/d0d5bafbb437d2150d590a45a118ccf75c4bb311/dicio/dicio.py

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
    def remove_tags(html):
        return re.sub("<[^>]*>", " ", html).strip()

    @staticmethod
    def text_between(text, before, after, force_html=False):
        start = text.find(before)
        if start > -1:
            start += len(before)
        if force_html:
            if before[-1] != ">":
                start = text.find(">", start) + 1
        end = text.find(after, start)
        if force_html:
            if after[0] != "<":
                end = text.find("<", start)
        if -1 < start < end:
            return text[start:end]
        return text.strip().lower()

    @staticmethod
    def remove_spaces(text):
        return re.sub("[\t\n\r ]+", " ", text).strip()

    @staticmethod
    def remove_accents(text):
        return unidecode(text)

    @staticmethod
    def split_html_tag(text, tag):
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

    def __repr__(self):
        return "{!r}".format(self.word)

    def __str__(self):
        return self.word


class Dicio:
    async def _request(self, word):
        if len(word.split()) > 1:
            return None
        _word = Utils.remove_accents(word).strip().lower()
        try:
            response = await asyncrq.get(BASE_URL.format(_word), res_method="text")
            return html.unescape(response)
        except:
            return None

    def _scrape_meaning(self, page):
        html = Utils.text_between(page, *TAG_MEANING, force_html=True)
        etymology = Utils.text_between(html, *TAG_ETYMOLOGY, force_html=True)
        etymology = Utils.remove_spaces(Utils.remove_tags(etymology))
        meanings = Utils.split_html_tag(html, "br")
        meanings = [Utils.remove_spaces(Utils.remove_tags(x)) for x in meanings]
        meaning = "; ".join([x for x in meanings if x != etymology])
        return meaning, etymology

    def _first_synonym(self, html):
        synonym = Utils.text_between(html, *TAG_SYNONYMS_DELIMITER, force_html=True)
        synonym = Utils.remove_spaces(synonym)
        _html = html.replace(TAG_SYNONYMS_DELIMITER[0], "", 1)
        _html = _html.replace(TAG_SYNONYMS_DELIMITER[1], "", 1)
        return Word(synonym), _html

    def _scrape_synonyms(self, page):
        synonyms = []
        if page.find(TAG_SYNONYMS[0]) > -1:
            html = Utils.text_between(page, *TAG_SYNONYMS, force_html=True)
            while html.find(TAG_SYNONYMS_DELIMITER[0]) > -1:
                synonym, html = self._first_synonym(html)
                synonyms.append(synonym)
        return synonyms

    def _scrape_examples(self, page):
        examples = []
        html = page
        index = html.find(TAG_PHRASE_DELIMITER[0])
        while index > -1:
            example_html = Utils.text_between(html, *TAG_PHRASE_DELIMITER, force_html=True)
            examples += [Utils.remove_spaces(Utils.remove_tags(example_html))]
            html = html[index + len(TAG_PHRASE_DELIMITER[0]) :]
            index = html.find(TAG_PHRASE_DELIMITER[0])
        return examples

    def _scrape_extra(self, page):
        dict_extra = {}
        try:
            if page.find(TAG_EXTRA[0]) > -1:
                html = Utils.text_between(page, *TAG_EXTRA, force_html=True)
                extra_rows = Utils.split_html_tag(Utils.remove_spaces(html), TAG_EXTRA_SEP)
                for row in extra_rows:
                    _row = Utils.remove_tags(row)
                    key, value = map(Utils.remove_spaces, _row.split(":"))
                    dict_extra[key] = value
        except:
            pass
        return dict_extra

    async def exists(self, word):
        page = await self._request(word)
        title = Utils.text_between(page, "<h1", "</h1>", force_html=True)
        return unidecode(title) == unidecode(word)
    
    async def search(self, word):
        page = await self._request(word)
        meaning, etymology = self._scrape_meaning(page)
        return Word(
            Utils.text_between(page, "<h1", "</h1>", force_html=True),
            meaning=meaning,
            etymology=etymology,
            synonyms=self._scrape_synonyms(page),
            examples=self._scrape_examples(page),
            extra=self._scrape_extra(page),
        )

    async def meaning(self, word):
        page = await self._request(word)
        meaning, _ = self._scrape_meaning(page)
        return meaning

    async def synonyms(self, word):
        page = await self._request(word)
        return self._scrape_synonyms(page)
