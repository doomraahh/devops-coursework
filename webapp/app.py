"""
Простое Flask-приложение с A/B-тестом кнопки призыва к действию (CTA).

Логика:
- Каждому новому посетителю случайно назначается вариант A или B
  (сохраняется в cookie, чтобы при повторных заходах видеть тот же вариант).
- Каждый показ страницы -> +1 к "impressions" выбранного варианта.
- Каждый клик по кнопке -> +1 к "clicks" выбранного варианта (через /click).
- /stats показывает конверсию (clicks / impressions) по каждому варианту -
  это и есть результат A/B-теста.
"""
import json
import os
import random
import threading
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, make_response

app = Flask(__name__)

DATA_DIR = Path(os.environ.get("DATA_DIR", "/app/data"))
DATA_FILE = DATA_DIR / "stats.json"
LOCK = threading.Lock()

VARIANTS = {
    "A": {
        "headline": "Купить сейчас",
        "button_color": "#2563eb",  # синяя кнопка
        "button_text": "Купить",
    },
    "B": {
        "headline": "Успей взять по скидке!",
        "button_color": "#16a34a",  # зелёная кнопка
        "button_text": "Купить сейчас со скидкой",
    },
}


def _load_stats():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"A": {"impressions": 0, "clicks": 0}, "B": {"impressions": 0, "clicks": 0}}


def _save_stats(stats):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = DATA_FILE.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    tmp.replace(DATA_FILE)


def _bump(variant: str, field: str):
    with LOCK:
        stats = _load_stats()
        stats[variant][field] += 1
        _save_stats(stats)
        return stats


@app.route("/")
def index():
    variant = request.cookies.get("ab_variant")
    is_new_visitor = variant not in VARIANTS
    if is_new_visitor:
        variant = random.choice(list(VARIANTS.keys()))

    if is_new_visitor:
        _bump(variant, "impressions")

    resp = make_response(render_template("index.html", variant=variant, **VARIANTS[variant]))
    if is_new_visitor:
        resp.set_cookie("ab_variant", variant, max_age=60 * 60 * 24 * 30)
    return resp


@app.route("/click", methods=["POST"])
def click():
    variant = request.cookies.get("ab_variant")
    if variant not in VARIANTS:
        variant = random.choice(list(VARIANTS.keys()))
    stats = _bump(variant, "clicks")
    return jsonify({"ok": True, "variant": variant, "stats": stats})


@app.route("/stats")
def stats():
    data = _load_stats()
    report = {}
    for name, s in data.items():
        impressions = s["impressions"]
        clicks = s["clicks"]
        rate = (clicks / impressions * 100) if impressions else 0.0
        report[name] = {**s, "conversion_rate": round(rate, 2)}
    if request.args.get("format") == "json":
        return jsonify(report)
    return render_template("stats.html", report=report)


@app.route("/reset", methods=["POST"])
def reset():
    """Сброс статистики - удобно перед демонстрацией/тестами."""
    _save_stats({"A": {"impressions": 0, "clicks": 0}, "B": {"impressions": 0, "clicks": 0}})
    return redirect("/stats")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
