# -*- coding: utf-8 -*-
def greet():
    import pickle
    with open('cities.pickle', 'rb') as f:
        cities = pickle.load(f)
    text = "Привет! Напишите город из списка, в котором вы хотели бы пойти на концерт группы \"некондиция\":"
    for i in range(len(cities)):
        text = text + ' ' + cities[i]
        if i < len(cities) - 1:
            text = text + ','
        else:
            text = text + '.'
    return text

    
def message(text):
    import pickle
    text = text.lower()
    first_msg = False
    has_attachment = False

    with open('concert.pickle', 'rb') as f:
        answers = pickle.load(f)
    if text in answers:
        has_attachment = True
        
    if text[:4] == 'пока' \
    or text[:7] == 'до свид' \
    or text[:6] == 'досвид' \
    or text[:3] == 'бай' \
    or text[:6] == 'прощай':
        text = 'пока'
        first_msg = True
        
    answers['пока'] = "Увидимся на концертах!"
    
    response = "Боюсь, я вас не понял."
    if text not in answers:
        with open('cities.pickle', 'rb') as f:
            cities = pickle.load(f)
        response = response + (" Если вы хотите узнать о концерте группы \"некондиция\", "
                    "отправьте сообщение, которое содержит только название одного из городов тура:")
        for i in range(len(cities)):
            response = response + ' ' + cities[i]
            if i < len(cities) - 1:
                response = response + ','
            else:
                response = response + '.'
        response = response + " Если хотите закончить сессию, напишите \"пока\"."
    
            
    return first_msg, has_attachment, answers.get(text, response)


def attachment_photo(city):
    import pickle
    with open('photos.pickle', 'rb') as f:
        attachments = pickle.load(f)
    default_photo = 'photo-175556159_456239023'
    return attachments.get(city, default_photo)