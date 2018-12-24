# -*- coding: utf-8 -*-
import vk_api
import requests
from msg import greet, attachment_photo, message
from manager import greet_manager, new_gig

session = vk_api.VkApi(token=<ACCESS_TOKEN>)

action_code_text = 4
sent_message_flag = 2
manager_id = 22214286
first_msg = True
manager_as_customer = False

data = session.method(
    'messages.getLongPollServer',
    {'access_token': <ACCESS_TOKEN>}
)

users = {} # здесь будут храниться собеседники бота
while True:
    # отправление запроса на Long Poll сервер со временем ожидания 90 и опциями ответа 2
    response = requests.get(
        'https://{server}?act=a_check&key={key}&ts={ts}&wait=90&mode=2&version=2'.format(
            server=data['server'], key=data['key'], ts=data['ts'])).json()
    updates = response['updates']
    if updates:  # проверка, были ли обновления
        for element in updates:  # проход по всем обновлениям в ответе
            if element[0] == action_code_text and not element[2] & sent_message_flag: # входящее текстовое сообщение
                user_id = element[3]  # id собеседника
                text = element[5] # текст сообщения
                if user_id not in users:
                    users[user_id] = True # обозначим, что это новый собеседник
                
                if text == '@' and user_id == manager_id: # специальный знак для смены режима
                    users[user_id] = True
                    manager_as_customer = not manager_as_customer
                
                first_msg = users[user_id]
                try:
                    if user_id == manager_id and not manager_as_customer:
                        if first_msg:
                            # предложим внести информацию о новом концерте
                            users[user_id] = False
                            session.method('messages.send', {
                                'user_id': user_id,
                                'random_id': data['ts'] % 10000,
                                'message': greet_manager()
                            })
                        else: # обработаем информацию о новом концерте
                            if text == '@':
                                manager_as_customer = True
                                users[user_id] = True
                            else:
                                session.method('messages.send', {
                                    'user_id': user_id,
                                    'random_id': data['ts'] % 10000,
                                    'message': new_gig(text)
                                })
                        
                    elif first_msg: # предложим выбрать город
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
                                'attachment': attachment_photo(text.lower())
                            })
                        else:
                            session.method('messages.send', {
                                'user_id': user_id,
                                'random_id': data['ts'] % 10000,
                                'message': answer
                            })
                except:
                    session.method('messages.send', {
                        'user_id': user_id,
                        'random_id': data['ts'] % 10000,
                        'message': "Боюсь, я вас не понял. Пожалуйста, проверьте своё сообщение."
                    })
                
    data['ts'] = response['ts']  # обновление номера последнего обновления