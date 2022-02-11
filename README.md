# Отправка уведомлений о проверенных работах на сайте Devman.

Сервис отправки сообщений в телеграм о проверенных работах на сайте [dvmn.org](https://dvmn.org/).

## Как установить:

Скачать все файлы на свой компьютер. 

### Установить зависимости:

Python3 должен быть уже установлен. Далее использовать `pip` (или `pip3`, есть
конфликт с python2) для установки зависимостей:

```
pip install -r requirements.txt
```

## Как использовать:

Для работы сервиса необходимо создать файл `.env` рядом с файлом `main.py` и прописать
в нем настройки в формате `КЛЮЧ='ЗНАЧЕНИЕ'`

Необходимые настройки:
- `DEVMAN_TOKEN` — токен с сайта devman.org можно получить в разделе
[dvmn.org/api/docs/](https://dvmn.org/api/docs/).
- `TELEGRAM_TOKEN` — токен телеграм-бота.
- `CHAT_ID` — `chat_id` на который будут отправляться уведомления. Чтобы узнать свой 
`chat_id` можно написать боту `@userinfobot`.

После этого необходимо запустить проект в терминале командой:

```sh
python main.py
```

## Цель проекта:

Код написан в образовательных целях на курсе для
web-разработчиков [dvmn.org](https://dvmn.org/).
