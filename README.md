# Сила Тайги Бот

Telegram-бот для управления бонусной системой и взаимодействия с пользователями салона "Сила Тайги". Бот позволяет пользователям накапливать бонусы за посещения, запрашивать коды услуг и подарков, а также администраторы могут подтверждать эти коды.

## Функциональность

### Для пользователей:

- **/start**: Начать взаимодействие с ботом.
- **/help**: Показать список доступных команд.
- **Сгенерировать код услуги**: Сгенерировать код для получения услуги.
- **Проверить бонусы**: Проверить количество накопленных бонусов.
- **Сгенерировать код подарка**: Сгенерировать код для получения подарка.

### Для администраторов:

- **/admin**: Показать инструкции для администраторов.
- **/confirm <code>**: Подтвердить код услуги.
- **/confirmgift <code>**: Подтвердить код подарка.

## Установка и настройка

1. **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/ваш-аккаунт/силатаиги-бот.git
    cd силатаиги-бот
    ```

2. **Создайте виртуальное окружение и активируйте его:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate   # Для Windows: .venv\Scripts\activate
    ```

3. **Установите необходимые зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Инициализируйте базу данных:**
    Убедитесь, что скрипт `db.py` содержит функцию `init_db`, которая создаёт необходимые таблицы в базе данных. Функция вызывается при старте приложения.

5. **Заполните файл конфигурации:**
    В `bot.py` замените `ВАШ_ТОКЕН` на токен вашего Telegram-бота. Добавьте ID администраторов в список `ADMIN_IDS`.

6. **Запустите бота:**
    ```bash
    python bot.py
    ```

## Структура проекта

```
силатаиги-бот/
├── SilaTaigi_Bot/
│   ├── __init__.py
│   ├── bot.py
│   ├── db.py
│   └── requirements.txt
└── README.md
```

### Основные файлы:

- **bot.py**: Основная логика работы бота.
- **db.py**: Логика работы с базой данных.

## Инструкции для администраторов

Когда пользователь запрашивает код услуги, администратор получает сообщение от бота с этим кодом. Для подтверждения кода услуги администратор вводит команду в чат с ботом: `/confirm <code>`, заменяя `<code>` на фактический код.

Когда пользователь запрашивает код подарка, администратор также получает сообщение от бота с этим кодом. Для подтверждения кода подарка администратор вводит команду в чат с ботом: `/confirmgift <code>`, заменяя `<code>` на фактический код.
