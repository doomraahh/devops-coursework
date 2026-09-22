"""
Скрипт для демонстрации A/B-теста: имитирует N визитов реальных пользователей
на запущенное приложение (docker compose up) со случайным разделением на
варианты A/B и разной вероятностью "покупки" в каждом варианте, чтобы
на /stats было видно статистически значимую разницу.

Запуск (когда docker compose уже поднят на 80 порту):
    python3 simulate_traffic.py --host http://localhost --visits 400
"""
import argparse
import random

import requests

# Вариант B в этой симуляции сделан "удачным" - выше вероятность клика.
CLICK_PROBABILITY = {"A": 0.12, "B": 0.20}


def simulate(host: str, visits: int):
    for _ in range(visits):
        session = requests.Session()
        session.get(f"{host}/")  # заходит на сайт -> засчитывается impression
        variant = session.cookies.get("ab_variant")
        if variant and random.random() < CLICK_PROBABILITY.get(variant, 0):
            session.post(f"{host}/click")

    stats = requests.get(f"{host}/stats", params={"format": "json"}).json()
    print("Итоговая статистика A/B-теста:")
    for name, s in stats.items():
        print(f"  Вариант {name}: показов={s['impressions']}, "
              f"кликов={s['clicks']}, конверсия={s['conversion_rate']}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="http://localhost")
    parser.add_argument("--visits", type=int, default=400)
    args = parser.parse_args()
    simulate(args.host, args.visits)
