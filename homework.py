import os
import requests
import telegram
import time
from dotenv import load_dotenv


load_dotenv()

HOMEWORK_STATUSES = {
    'rejected': False,
    'approved': True
}

ERROR_MSG = 'Неверный ответ сервера'

API_URL = 'https://praktikum.yandex.ru/api/user_api'

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_PROXY = os.getenv('TELEGRAM_PROXY')

PROXY = telegram.utils.request.Request(
    proxy_url=TELEGRAM_PROXY)

BOT = telegram.Bot(token=TELEGRAM_TOKEN, request=PROXY)


def parse_homework_status(homework):

    homework_name = homework.get('homework_name')
    homework_status_response = homework.get('status')
    homework_status = HOMEWORK_STATUSES.get(homework_status_response)

    if homework_status is None or homework_name is None:
        return ERROR_MSG

    if not homework_status:
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'

    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):

    if current_timestamp == None:
        current_timestamp = int(time.time())

    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    statuses_url = '{}/{}/'.format(API_URL, 'homework_statuses')

    try:

        homework_statuses = requests.get(
            statuses_url, headers=headers, params=params)

    except requests.RequestException as e:
        print(f'Бот упал с ошибкой: {e}')

    try:
        homework_stauses_json_data = homework_statuses.json()
    except ValueError as e:
        print(f'Ошибка парсинга JSON: {e}')
        homework_stauses_json_data = {}

    return homework_stauses_json_data


def send_message(message):

    try:
        result = BOT.send_message(chat_id=CHAT_ID, text=message)
    except telegram.error.TelegramError as telegram_error:
        print(f'Ошибка отправки сообещния через Telegram: {telegram_error}')
        result = None

    return result


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
            time.sleep(300)

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(15)
            continue


if __name__ == '__main__':
    main()
