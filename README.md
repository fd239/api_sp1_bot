# Yandex API telegram bot

Yandex training project. A telegram bot that checks the status of homework from Yandex via the API and sends messages if the status has changed

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Project depends from .env file in root folder. File .env must contain tokens, chat ID with user and proper telegram proxy

```
PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
```

### Installing

```
pip install -r requirements.txt
```

## Running the tests

Project covered with Pytest tests

### Break down into end to end tests

```
pytest
```

### And coding style tests

It's learning project so test are aimed at checking the fulfillment of a test task

```
 def test_parse_homework_status(self, random_sid):
        test_data = {
            "id": 123,
            "status": "approved",
            "homework_name": str(random_sid),
            "reviewer_comment": "Всё нравится",
            "date_updated": "2020-02-13T14:40:57Z",
            "lesson_name": "Итоговый проект"
        }

        import homework

        assert hasattr(homework, 'parse_homework_status'), \
            'Функция `parse_homework_status()` не существует. Не удаляйте её.'
        assert hasattr(homework.parse_homework_status, '__call__'), \
            'Функция `parse_homework_status()` не существует. Не удаляйте её.'
        assert len(signature(homework.parse_homework_status).parameters) == 1, \
            'Функция `parse_homework_status()` должна быть с одним параметром.'
```

## Built With

* [Python telegram bot](https://pypi.org/project/python-telegram-bot/) - Python interface for the Telegram Bot API
* [Yandex Praktikum](https://praktikum.yandex.ru/) - Test tasks and all test in project

## Authors

* **Yandex Praktikum** - *Test task and tests cover* - [yandex-praktikum](https://github.com/yandex-praktikum)
* **Dmitriy Frolov** - *Connection and interaction with Yandex API and Telegram API* - [fd239](https://github.com/fd239)
