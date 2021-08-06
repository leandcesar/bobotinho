# -*- coding: utf-8 -*-
from collections import namedtuple


def create_afks():
    keys = ["emoji", "afk", "isafk", "returned", "rafk"]
    values = [
        ["afk", "🏃⌨", "ficou AFK", "AFK", "voltou", "AFK"],
        ["art", "🎨", "foi desenhar", "desenhando", "desenhou", "desenhando"],
        ["brb", "🏃⌨", "volta já", "fora", "voltou", "fora"],
        ["code", "💻", "foi programar", "programando", "programou", "programando"],
        ["food", "🍽", "foi comer", "comendo", "comeu", "comendo"],
        ["game", "🎮", "foi jogar", "jogando", "jogou", "jogando"],
        ["gn", "💤", "foi dormir", "dormindo", "acordou", "dormindo"],
        ["work", "💼", "foi trabalhar", "trabalhando", "trabalhou", "trabalhando"],
        ["read", "📖", "foi ler", "lendo", "leu", "lendo"],
        ["shower", "🚿", "foi pro banho", "no banho", "tomou banho", "o banho"],
        ["study", "📚", "foi estudar", "estudando", "estudou", "estudando"],
        ["watch", "📺", "foi assistir", "assistindo", "assistiu", "assistindo"],
    ]
    return {value[0]: namedtuple(value[0], keys)(*value[1:]) for value in values}


afks = create_afks()
