# -*- coding: utf-8 -*-
import json
import random
from collections import namedtuple
from datetime import datetime

FILENAME = "bobotinho//data//pets.json"


def create_pet(pet: dict) -> object:
    return namedtuple("Pet", pet.keys())(**pet)


def create_pets() -> dict:
    with open(FILENAME, "r", encoding="utf-8") as file:
        return {
            pet["specie"]: create_pet(pet)
            for pet in json.load(file)
        }


def random_pets(limit: int = 7) -> dict:
    now = datetime.utcnow()
    random.seed(now.day + now.month)
    pets = random.sample(all_pets.items(), limit)
    random.seed(None)
    return dict(pets)


def join_pets(pets: object, formatter: str, sep: str = " ") -> str:
    return sep.join(
        formatter.format(
            pet=getattr(pet, "name", pet.specie) or pet.specie,
            emoji=getattr(pet, "emoji", all_pets[pet.specie].emoji),
            price=getattr(pet, "price", all_pets[pet.specie].price)
        )
        for pet in pets
    )


all_pets = create_pets()
