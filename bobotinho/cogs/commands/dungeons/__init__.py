# -*- coding: utf-8 -*-
import json
import random
from typing import Optional

FILENAME = "bobotinho//data//dungeons.json"


def create_classes():
    __w_M_A = [
        "Guerreiro",
        "Mercenário",
        "Cavaleiro",
        "Lord",
        "Grão Mestre",
        "Imperador da Espada",
        "Guardião Divino",
    ]
    __w_M_B = [
        "Guerreiro",
        "Mercenário",
        "Cavaleiro",
        "Cavaleiro das Trevas",
        "Guerreiro Arcano",
        "Demônio da Espada",
        "Ascendente Imortal",
    ]
    __w_F_A = [
        "Guerreira",
        "Mercenária",
        "Cavaleira",
        "Lord",
        "Grã Mestra",
        "Imperatriz da Espada",
        "Guardiã Divina",
    ]
    __w_F_B = [
        "Guerreira",
        "Mercenária",
        "Cavaleira",
        "Cavaleira das Trevas",
        "Guerreira Arcana",
        "Demônia da Espada",
        "Ascendente Imortal",
    ]
    __a_M_A = [
        "Arqueiro",
        "Atirador de Elite",
        "Sentinela",
        "Domador Bestial",
        "Caçador de Demônios",
        "Maestro dos Ventos",
        "Aurora dos Deuses",
    ]
    __a_M_B = [
        "Arqueiro",
        "Atirador de Elite",
        "Sentinela",
        "Caçador",
        "Assassino Arcano",
        "Sombra Viva",
        "Crepúsculo dos Deuses",
    ]
    __a_F_A = [
        "Arqueira",
        "Atiradora de Elite",
        "Sentinela",
        "Domadora Bestial",
        "Caçadora de Demônios",
        "Maestrina dos Ventos",
        "Aurora dos Deuses",
    ]
    __a_F_B = [
        "Arqueira",
        "Atiradora de Elite",
        "Sentinela",
        "Caçadora",
        "Assassina Arcana",
        "Sombra Viva",
        "Crepúsculo dos Deuses",
    ]
    __m_M_A = [
        "Mago",
        "Feiticeiro",
        "Mestre Elemental",
        "Alquimista",
        "Ladrão de Mentes",
        "Necromante",
        "Lich",
    ]
    __m_M_B = [
        "Mago",
        "Feiticeiro",
        "Mestre Elemental",
        "Clérigo",
        "Arcebispo",
        "Conjurador dos Divinos",
        "Anjo",
    ]
    __m_F_A = [
        "Maga",
        "Feiticeira",
        "Mestra Elemental",
        "Alquimista",
        "Ladra de Mentes",
        "Necromante",
        "Lich",
    ]
    __m_F_B = [
        "Maga",
        "Feiticeira",
        "Mestra Elemental",
        "Clériga",
        "Arcebispa",
        "Conjuradora dos Divinos",
        "Anjo",
    ]
    return {
        "w": {
            "M": {"A": __w_M_A, "B": __w_M_B},
            "F": {"A": __w_F_A, "B": __w_F_B},
            "emoji": "⚔️",
        },
        "a": {
            "M": {"A": __a_M_A, "B": __a_M_B},
            "F": {"A": __a_F_A, "B": __a_F_B},
            "emoji": "🏹",
        },
        "m": {
            "M": {"A": __m_M_A, "B": __m_M_B},
            "F": {"A": __m_F_A, "B": __m_F_B},
            "emoji": "🧙",
        },
    }


classes = create_classes()


def generate_dungeon(i: int = None) -> (dict, int):
    with open(FILENAME, "r", encoding="utf-8") as file:
        dicts = json.load(file)
    i = int(i) if i else random.randint(0, len(dicts) - 1)
    return dicts[i], i


def resume_dungeon(dungeon: object, choice: str = None) -> (object, str):
    d = generate_dungeon(dungeon.i)[0]
    result = random.choices(["win", "lose"], weights=(0.66, 0.33), k=1)[0]
    if not choice:
        choice = random.choice(["1", "2"])
        quote, options = d["quote"].split('"%ed 1"')
        option = options.split('ou "%ed 2"')[int(choice) - 1].replace("para", "Você decide", 1).rstrip()
        response = quote + option + ". "
        response += d[choice][result]
    else:
        response = d[choice][result]
    if result == "win":
        dungeon.wins += 1
        gained = random.randint(50, 75) + 3 * dungeon.level
        dungeon.xp += gained
        response += f" +{gained} XP"
        if dungeon.xp > 100 * (dungeon.level) + 25 * sum(range(1, dungeon.level + 1)):
            dungeon.level += + 1
            if dungeon.level % 10 == 0 and dungeon.level < 70:
                response += f", alcançou level {dungeon.level} ⬆"
                if dungeon.level == 30:
                    op1, op2 = options_sub_class(dungeon.class_, dungeon.gender)
                    dungeon.sub_class = None
                    response += f" e pode se tornar {op1} ou {op2}!"
                else:
                    c = classes[dungeon.class_][dungeon.gender][dungeon.level // 10]
                    response += f" e se tornou {c}"
            else:
                response += f" e alcançou level {dungeon.level} ⬆"
    else:
        dungeon.defeats += 1
        response += " 0 XP"
    dungeon.i = None
    return (dungeon, response)


def options_class() -> dict:
    initial_classes = {}
    for class_, c in classes.items():
        initial_classes[c["M"]["A"][0]] = {
            "class_": class_,
            "gender": "M",
        }
        initial_classes[c["F"]["A"][0]] = {
            "class_": class_,
            "gender": "F",
        }
    return initial_classes


def options_sub_class(class_: str, gender: str) -> list:
    option_A = classes[class_][gender]["A"][3]
    option_B = classes[class_][gender]["B"][3]
    return (option_A, option_B)


def choose_class(choice: str) -> Optional[str]:
    options = options_class()
    for option, values in options.items():
        if choice == option.lower():
            return values


def choose_sub_class(choice: str, class_: str, gender: str) -> Optional[str]:
    options = options_sub_class(class_, gender)
    if choice == options[0].lower():
        return "A"
    if choice == options[1].lower():
        return "B"
