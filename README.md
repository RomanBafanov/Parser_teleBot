# Parser_teleBot

## Описание

Parser_teleBot - это Telegram-бот, который помогает вам найти работу.
Бот ищет сайты, номера телефонов и компании, соответствующие названиям вакансий
и желаемому местоположению, затем отправляет вам эксель файл с данными.

## Установка

**1. Python:**

Убедитесь, что у вас установлен Python 3.10.

**2. Зависимости:**

Используйте `pip` для установки зависимостей:

pip install -r requirements.txt


**3. Создание бота:**

* **BotFather:** Зайдите в Telegram и найдите бота BotFather.
* **Создание:** Введите команду /newbot и следуйте инструкциям, чтобы создать нового бота.
* **Токен:** Вам будет предоставлен токен бота, который нужно сохранить в файле .env (BOT_TOKEN).

**4. Настройка PostgreSQL:**

* Установите PostgreSQL (можно использовать PgAdmin4).
* **Создание пользователя и пароля:** Создайте пользователя и пароль для доступа к базе данных.
* **Сохранение данных:** Запишите имя пользователя, пароль и имя базы данных в файле .env.

**5. Создание базы данных и таблиц:**

* **create_db.py:** Запустите этот файл, чтобы создать базу данных.
* **create_tables.py:** Запустите этот файл, чтобы создать таблицы в базе данных.
* **Filling_cities.py:** Запустите этот файл, чтобы заполнить таблицу городов.

## Запуск бота

* **main.py:** Запустите этот файл, чтобы запустить бота.

  