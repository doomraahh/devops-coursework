1. Проект на Linux + Docker (веб-сервер).
2. A/B-тесты системы.
3. CI/CD для Android-приложения и desktop-приложения.
4. Тестирование python.org с помощью Selenium + pytest.

Стек: Python (Flask, Tkinter), Docker/Docker Compose, Nginx, Kotlin (Android), GitHub Actions.

## Структура репозитория

```
webapp/             Flask-приложение с A/B-тестом кнопки покупки
nginx/               Nginx как reverse proxy перед Flask
docker-compose.yml    Поднимает web + nginx одной командой
selenium-tests/      Selenium + pytest тесты для https://www.python.org
android-app/         Минимальное Android-приложение (Kotlin) + unit-тест
desktop-app/         Минимальное desktop-приложение (Tkinter) + unit-тест
.github/workflows/    4 пайплайна CI/CD (см. ниже)
```

## 1. Веб-проект в Docker + A/B-тест

Поднять стек (Flask-приложение за Nginx):

```bash
cd devops-coursework
docker compose up -d --build
```

Приложение доступно на `http://<IP-сервера>/`. При каждом новом визите
случайно назначается вариант **A** (кнопка "Купить") или **B** (кнопка
"Купить сейчас со скидкой"), назначение закрепляется в cookie. Клик по
кнопке фиксируется на бэкенде.

Результаты теста: `http://<IP-сервера>/stats`

Чтобы быстро сгенерировать наглядную статистику для демонстрации
(симулирует несколько сотен визитов с разной вероятностью клика по
вариантам):

```bash
python3 -m pip install requests
python3 webapp/simulate_traffic.py --host http://localhost --visits 500
```

После этого откройте `/stats` — будет видно, какой вариант выигрывает
по конверсии.

Остановить стек: `docker compose down`

## 2. Selenium + pytest тесты python.org

```bash
cd selenium-tests
python3 -m pip install -r requirements.txt
pytest -v
```

5 тестов проверяют: главную страницу, поиск по сайту, переход в
Downloads, переход в Documentation, блок последних новостей. 

## 3. Android-приложение + CI/CD

`android-app/` — минимальный проект с тем же A/B-сценарием (случайный
вариант кнопки), логика выбора варианта вынесена в `AbVariant.kt` и
покрыта unit-тестом `AbVariantTest.kt`.

Чтобы работать с проектом в Android Studio: `File -> Open` -> выбрать
папку `android-app`. IDE подтянет Gradle-зависимости сама.

CI/CD (`.github/workflows/android-ci.yml`) при каждом пуше в ветку
`main`:
- собирает проект,
- прогоняет unit-тесты,
- собирает debug APK и прикладывает его как build-артефакт GitHub
  Actions.

Сборка происходит в облаке (GitHub Actions).

## 4. Desktop-приложение + CI/CD

`desktop-app/` — Tkinter-приложение с тем же A/B-сценарием, логика
(`ab_logic.py`) отделена от GUI и покрыта тестами (`test_ab_logic.py`).

Запуск локально (нужен графический дисплей):

```bash
cd desktop-app
python3 app.py
```

CI/CD (`.github/workflows/desktop-ci.yml`):
- прогоняет pytest для бизнес-логики (без GUI, без дисплея),
- собирает готовые исполняемые файлы под Linux и Windows через
  PyInstaller и прикладывает их как build-артефакты.



