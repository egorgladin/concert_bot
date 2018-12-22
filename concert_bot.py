import vk_api
import requests
import time

session = vk_api.VkApi(token=<ACCES_TOKEN>)

data = session.method('messages.getLongPollServer', {'access_token': <ACCES_TOKEN>})

first_msg = True

while True:
    # отправление запроса на Long Poll сервер со временем ожидания 90 и опциями ответа 2
    response = requests.get(
		'https://{server}?act=a_check&key={key}&ts={ts}&wait=90&mode=2&version=2'.format(
		server=data['server'], key=data['key'], ts=data['ts'])).json()
    updates = response['updates']
    if updates:  # проверка, были ли обновления
        for element in updates:  # проход по всем обновлениям в ответе
            action_code = element[0]  # запись в переменную кода события
            flag = element[2]  # флаг сообщения
            
            if action_code == 4 and not (flag & 2) and first_msg: # пришло первое сообщение - предложим выбрать город
                user_id = element[3]  # id собеседника
                text = element[5]
                first_msg = False
                session.method('messages.send', {
                    'user_id': user_id,
                    'random_id': data['ts'] % 10000,
                    'message': ("Напишите город из списка, в котором вы хотели бы пойти на концерт: "
                                "Москва, Санкт-Петербург, Екатеринбург, Нижний Новгород."
                               )
                })
            
            elif action_code == 4 and not (flag & 2): # пришло входящее сообщение
                user_id = element[3]  # id собеседника
                text = element[5]
                
                if text.lower() == 'москва':
                    session.method('messages.send', {
                        'user_id': user_id,
                        'random_id': data['ts'] % 10000,
                        'message': ("Концерт в Москве пройдёт 7 января в клубе Punk Fiction. "
                                    "Адрес клуба: м. Бауманская/Красносельская, ул. Ольховская, 14с1. "
                                    "Билеты можно приобрести в кассе клуба по цене 400р. "
                                    "Начало концерта в 19:00"
                                   )
                    })
                    first_msg = True
                elif text.lower() == 'санкт-петербург':
                    session.method('messages.send', {
                        'user_id': user_id,
                        'random_id': data['ts'] % 10000,
                        'message': ("Концерт в Питере пройдёт 8 января в клубе Zoccolo 2.0. "
                                    "Адрес клуба: м. Площадь Восстания, Лиговский пр-т, 50к3 "
                                    "Билеты можно приобрести в кассе клуба по цене 350р."
                                    "Начало концерта в 19:00"
                                   )
                    })
                    first_msg = True
                elif text.lower() == 'екатеринбург':
                    session.method('messages.send', {
                        'user_id': user_id,
                        'random_id': data['ts'] % 10000,
                        'message': ("Концерт в Екатеринбурге пройдёт 9 января в клубе Оливер. "
                                    "Адрес клуба: ул. Комсомольская, 23 "
                                    "Билеты можно приобрести в кассе клуба по цене 300р."
                                    "Начало концерта в 19:00"
                                   )
                    })
                    first_msg = True
                elif text.lower() == 'нижний новгород':
                    session.method('messages.send', {
                        'user_id': user_id,
                        'random_id': data['ts'] % 10000,
                        'message': ("Концерт в Нижнем Новгороде пройдёт 10 января в клубе Volta. "
                                    "Адрес клуба: ул. Ленина, 65 "
                                    "Билеты можно приобрести в кассе клуба по цене 250р."
                                    "Начало концерта в 19:00"
                                   )
                    })
                    first_msg = True
                else:
                    session.method('messages.send', {
                        'user_id': user_id,
                        'random_id': data['ts'] % 10000,
                        'message': ("Боюсь, я вас не понял. Пожалуйста, отправьте сообщение, "
                                    "которое содержит только название одного из перечисленных городов: "
                                    "Москва, Санкт-Петербург, Екатеринбург, Нижний Новгород."
                                   )
                    })
                
    data['ts'] = response['ts']  # обновление номера последнего обновления