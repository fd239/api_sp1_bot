import os
import requests
import telegram
import time
from dotenv import load_dotenv
from boto.s3.connection import S3Connection

load_dotenv()


PRACTICUM_TOKEN = S3Connection(os.environ['PRACTICUM_TOKEN'])
TELEGRAM_TOKEN = S3Connection(os.environ['TELEGRAM_TOKEN'])
CHAT_ID = S3Connection(os.environ['TELEGRAM_CHAT_ID'])


def parse_homework_status(homework):
    homework_name = homework['homework_name']
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):

    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    params = {'from_date': current_timestamp}

    homework_statuses = requests.get(
        'https://praktikum.yandex.ru/api/user_api/homework_statuses/', headers=headers, params=params)

    return homework_statuses.json()


def send_message(message):
    proxy = telegram.utils.request.Request(
        proxy_url='socks5://75.119.217.119:25727')
    bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy)
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get(
                'current_date')
            time.sleep(1200)

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()