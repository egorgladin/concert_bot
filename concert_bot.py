import vk_api
import requests
import time
from msg import greet, message, attachment_photo

session = vk_api.VkApi(token=<ACCES_TOKEN>)

data = session.method('messages.getLongPollServer', {'access_token': <ACCES_TOKEN>})

action_code_text = 4
sent_message_flag = 2
first_msg = True

users = {} # здесь будут храниться собеседники бота
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
                text = element[5].lower() # текст сообщения
                if user_id not in users:
                    users[user_id] = True # обозначим, что это новый собеседник
                first_msg = users[user_id]
                
                if first_msg: # предложим выбрать город
                    users[user_id] = False
                    session.method('messages.send', {
                        'user_id': user_id,
                        'random_id': data['ts'] % 10000,
                        'message': greet()
                    })
                else:
                    users[user_id], has_attachment, answer = message(text)
                    if has_attachment:
                        session.method('messages.send', {
                            'user_id': user_id,
                            'random_id': data['ts'] % 10000,
                            'message': answer,
                            'attachment': attachment_photo(text)
                        })
                    else:
                        session.method('messages.send', {
                            'user_id': user_id,
                            'random_id': data['ts'] % 10000,
                            'message': answer
                        })
                    
    data['ts'] = response['ts']  # обновление номера последнего обновления