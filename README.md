# Game of verbs

Телеграм и vk бот для получения ответов на частые вопросы. Ответы генерируются через сервис 
[dialogflow](https://cloud.google.com/dialogflow).


## Установка

```commandline
git clone https://github.com/Weffy61/Game_of_verbs
```

## Установка зависимостей
Переход в директорию с исполняемым файлом

```commandline
cd Game_of_verbs
```

Установка
```commandline
pip install -r requirements.txt
```

## Предварительная подготовка

### Подготовка vk

Создайте группу в [vk](vk.com), получите [API для сообщений сообществ]
(https://dev.vk.com/ru/api/community-messages/getting-started?ref=old_portal), установите права доступа для сообщений 
сообщества. Включите сообщения сообщества в настройках группы.

### Подготовка telegram

Создайте 2 ботов в [botfather](https://t.me/BotFather). 1-ый бот будет отвечать на вопросы, 2-ой бот будет 
использоваться для мониторинга состояния бота в vk и 1-ого бота.

### Подготовка Dialogflow

Создайте DialogFlow [проект](https://cloud.google.com/dialogflow/es/docs/quick/setup). 
[Получите токен и credentials](https://cloud.google.com/docs/authentication/api-keys)


## Создание и настройка .env

Создайте в корне папки `Game_of_verbs` файл `.env`. Откройте его для редактирования любым текстовым редактором
и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступны следующие переменные:
 - TELEGRAM_BOT_API - ваш телеграм бот API ключ(бот, который отвечает на вопросы).
 - DIALOGFLOW_PROJECT_ID - Ваш id проекта. 
 - VK_API_KEY - Ваш vk API ключ(для бота, который отвечает на вопросы).
 - GOOGLE_APPLICATION_CREDENTIALS - путь до файла с ключами от Google, credentials.json.
 - TELEGRAM_LOGS_TOKEN - ваш телеграм бот API ключ(бот, который отправляет уведомления в личку/канал/чат, при наличии, 
каких-либо ошибок, а также уведомление о старте бота).
 - TELEGRAM_CHAT_ID - ваш telegram id  куда вы будете получать уведомления о  состоянии бота. Для получаения отпишите в 
[бота](https://telegram.me/userinfobot).
 
### Обучение DialogFlow

Для добвления новых фраз и связок слов создайте `json` файл, на примере вложенного файла `questions.json`.  
Запустите скрипт:

```commandline
python3 create_intent.py file
```
Аргумент:
file - путь к вашему файлу

Например:

```commandline
python3 create_intent.py test_file.json
```

Данный пример запустит обучение на основании файла `test_file.json`.
Также вы можете запустить скрипт без аргументов в ознакомитеном варианте:

```commandline
python3 create_intent.py
```

Скрипт запустится с ознакомительным файлом questions.json.

## Запуск телеграм бота

```commandline
python telegram_bot.py
```

Пример работы телеграм бота:  
![telegram example](https://dvmn.org/filer/canonical/1569214094/323/)

Образец бота:
https://t.me/Game_of_verbsbot

## Запуск бота в vk

```commandline
python vk_bot.py
```

Пример работы vk бота:

![vk example](https://dvmn.org/filer/canonical/1569214089/322/)

Образец бота:
https://vk.com/club224224921