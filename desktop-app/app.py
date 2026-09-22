"""
Минимальное десктоп-приложение (Tkinter) с тем же A/B-сценарием,
что и веб-версия: случайный вариант кнопки + счётчик кликов.

Запуск локально (нужен дисплей):
    python3 app.py
"""
import tkinter as tk

from ab_logic import pick_variant


def main():
    variant = pick_variant()
    clicks = {"count": 0}

    root = tk.Tk()
    root.title("AB Demo Desktop")
    root.geometry("360x200")

    tk.Label(root, text=f"Вариант: {variant.name}", font=("Arial", 14)).pack(pady=10)

    click_label = tk.Label(root, text="Кликов: 0")

    def on_click():
        clicks["count"] += 1
        click_label.config(text=f"Кликов: {clicks['count']}")

    tk.Button(
        root,
        text=variant.button_text,
        bg=variant.color,
        fg="white",
        command=on_click,
    ).pack(pady=10)

    click_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
