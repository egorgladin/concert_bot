import vk_api
import requests
import time
from msg import greet, message

session = vk_api.VkApi(token=<ACCES_TOKEN>)

data = session.method('messages.getLongPollServer', {'access_token': <ACCES_TOKEN>})

action_code_text = 4
sent_message_flag = 2
first_msg = True

while True:
    # отправление запроса на Long Poll сервер со временем ожидания 90 и опциями ответа 2
    response = requests.get(
        'https://{server}?act=a_check&key={key}&ts={ts}&wait=90&mode=2&version=2'.format(
            server=data['server'], key=data['key'], ts=data['ts'])
    ).json()
    updates = response['updates']
    if updates:  # проверка, были ли обновления
        for element in updates:  # проход по всем обновлениям в ответе
            if element[0] == action_code_text and not element[2] & sent_message_flag: # входящее текстовое сообщение
                user_id = element[3]  # id собеседника
                text = element[5] # текст сообщения
                if first_msg: # предложим выбрать город
                    first_msg = False
                    session.method('messages.send', {
                        'user_id': user_id,
                        'random_id': data['ts'] % 10000,
                        'message': greet()
                    })
                else:
                    first_msg, answer = message(text)
                    session.method('messages.send', {
                        'user_id': user_id,
                        'random_id': data['ts'] % 10000,
                        'message': answer
                    })
                    
    data['ts'] = response['ts']  # обновление номера последнего обновления