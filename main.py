import telegram
import requests
from dotenv import load_dotenv

import os
import time


def main():
    load_dotenv()

    long_polling_url = "https://dvmn.org/api/long_polling/"

    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    bot = telegram.Bot(token=telegram_token)

    headers = {
        f'Authorization': f'Token {devman_token}'
    }

    last_timestamp = time.time()

    text_result = {
        False: 'Все хорошо, можно приступать к следующему уроку',
        True: 'Еще есть над чем поработать',
    }

    while True:
        payload = {
            'timestamp': last_timestamp
        }
        try:
            response = requests.get(
                long_polling_url,
                headers=headers,
                params=payload,
                timeout=5
            )
            response.raise_for_status()
            last_attempt = response.json()

            if last_attempt['status'] == 'found':
                last_timestamp = last_attempt['last_attempt_timestamp']
                for lesson in last_attempt['new_attempts']:
                    result = text_result[lesson['is_negative']]
                    lesson_url = lesson["lesson_url"]

                    text = (
                        'Преподаватель проверил вашу работу \n'
                        f'"{lesson["lesson_title"]}" \n\n'
                        f'{result} \n\n'
                        f'<a href="{lesson_url}">Перейти к уроку</a> '
                    )

                    bot.send_message(
                        text=text,
                        chat_id=chat_id,
                        parse_mode='HTML'
                    )

        except requests.exceptions.ReadTimeout:
            pass
        except requests.ConnectionError:
            time.sleep(5)


if __name__ == '__main__':
    main()
