import telegram
import requests
from dotenv import load_dotenv

import os
import time
from pprint import pprint
load_dotenv()


def main():

    long_polling_url = "https://dvmn.org/api/long_polling/"
    polling_url = 'https://dvmn.org/api/user_reviews/'

    devman_token = os.getenv('DEVMAN_TOKEN')

    headers = {
        f'Authorization': f'Token {devman_token}'
    }

    timestamp_with_work = '1644420344.9888153'
    timestamp_with_few_works = '1555609162.580245'
    timestamp_without_works = '1644552707.1979823'

    #last_timestamp = time.time()
    last_timestamp = timestamp_with_work

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

        except requests.exceptions.ReadTimeout:
            print('Works not found')
            pass
        except OSError:
            pass


if __name__ == '__main__':
    main()
