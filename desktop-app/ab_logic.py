"""
Логика A/B-варианта для десктоп-приложения, отделена от GUI-кода,
чтобы её можно было тестировать через pytest без открытия окна
(на CI-раннере обычно нет дисплея).
"""
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Variant:
    name: str
    button_text: str
    color: str


VARIANTS = {
    "A": Variant(name="A", button_text="Купить", color="#2563eb"),
    "B": Variant(name="B", button_text="Купить сейчас со скидкой", color="#16a34a"),
}


def pick_variant(rng: random.Random | None = None) -> Variant:
    rng = rng or random.Random()
    return VARIANTS[rng.choice(list(VARIANTS.keys()))]
