from logic import *

connect = engine.connect()

last_update_id = 0

while True:
    result = requests.get(
            f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/getUpdates',
            params={'offset': last_update_id + 1})

    data = result.json() # ['ok', 'result'] or ['ok', 'error_code', 'description']
    try:
        for update in data['result']:
            last_update_id = update['update_id']
            chat_id = update['message']['chat']['id']
            message = update['message']['text']
            user_id = update['message']['from']['id']
            user_name = update['message']['from']['first_name']
            print(f' Telegram_Bot: message -[{message}] from [{user_name}]')
            if message == "/start":
            	saveUser(user_id, user_name, chat_id)
            	continue
            if message == "/me":
            	message = getUser(user_id)
            	send_message(chat_id, message)
            	continue
            if message == "/iin":
                send_message(chat_id, 'Хорошо, отправьте нам ИИН (в формате ИИН-****************)')
                continue
            if message[:4] == "ИИН-" and len(message) == 16:
                send_message(chat_id, getInfoByIIN(message[4:]))
                continue
            if message == "/tech":
            	print(f'\n{update}\n')
            	continue
            check = check_phone(message)
            if check != None:
            	composeMessage(chat_id=chat_id ,user_id=user_id, user_name=user_id, key='phone', check=check)
            else:
            	saveSearcher(telegram_id=user_id, search=message, user_name=user_name, key='command') 
            	message = 'Неверный формат!'
            	send_message(chat_id, message)
    except KeyError: print(f' Telegram_Bot: message error from {user_name} !')
    time.sleep(5)