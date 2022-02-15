import telegram
import requests
from dotenv import load_dotenv

import logging
import os
import time
from textwrap import dedent

logger = logging.getLogger('Logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()

    long_polling_url = "https://dvmn.org/api/long_polling/"
    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    bot = telegram.Bot(token=telegram_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(bot, telegram_chat_id))

    headers = {
        f'Authorization': f'Token {devman_token}'
    }

    last_timestamp = time.time()

    text_result = {
        False: 'Все хорошо, можно приступать к следующему уроку',
        True: 'Еще есть над чем поработать',
    }

    logger.warning('Бот запущен')

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

                    text = dedent(
                        f'''\
                            Преподаватель проверил вашу работу:
                            "{lesson["lesson_title"]}".
                        
                            {result}
                        
                            <a href="{lesson_url}">Перейти к уроку</a>
                        '''
                    )

                    bot.send_message(
                        text=text,
                        chat_id=telegram_chat_id,
                        parse_mode='HTML'
                    )
            elif last_attempt['status'] == 'timeout':
                last_timestamp = last_attempt['timestamp_to_request']

        except requests.exceptions.ReadTimeout:
            pass
        except requests.ConnectionError:
            time.sleep(5)
        except Exception:
            logging.exception('Непредвиденная ошибка:', exc_info=True)


if __name__ == '__main__':
    main()
