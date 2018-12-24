# -*- coding: utf-8 -*-
def greet_manager():
    return ("Здравствуйте, уважаемый менеджер.\n"
            "1. Если хотите внести информацию "
            "о новом концерте или обновить о существующем, напишите её в "
            "следующем порядке, соблюдая предложенную пунктуацию:\n"
            "вариации; названия; города | название города "
            "в именительном падеже; название города в предложном падеже; "
            "дата (число цифрами, название месяца словом); название "
            "клуба; адрес клуба; цена билета; время начала концерта; "
            "идентификатор фото. Пример:\n"
            "Москва; мск | Москва; Москве; 7 января; Punk Fiction; ул. "
            "Ольховская, 14с1; 400р; 19:00; photo-175556159_456239021\n"
            "2. Чтобы попасть в режим обычного пользователя, отправьте "
            "сообщение с символом \'@\'. Вы сможете в любой момент "
            "вернуться в режим менеджера, снова отправив \'@\'.")
            
def new_gig(data):
    import pickle
    if '~' in data:
        return "Пожалуйста, введите данные так, чтобы в них не содержалось знака \'~\'"
    if data.count('|') != 1:
        return "Согласно описанному выше формату, в сообщении должен быть только один знак \'|\'"
        
    data = data.replace(' | ', '|').replace('| ', '|').replace(' |', '|')
    keys = data.lower().split('|')[0].replace(' ; ', '~').replace('; ', '~').replace(' ;', '~').replace(';', '~').split('~')
    data = data.split('|')[1].replace(' ; ', '~').replace('; ', '~').replace(' ;', '~').replace(';', '~').split('~')
    
    if len(keys) == 0 or len(data) != 8:
        return "Боюсь, ваше сообщение не удовлетворяет формату. Пожалуйста, попробуйте снова."
    
    with open('concert.pickle', 'rb') as f:
        answers = pickle.load(f)
    
    answers.update(dict.fromkeys(keys,
             ("Концерт \"некондиции\" в {city} пройдёт {date} в клубе {club}. "
              "Адрес клуба: {adress}. "
              "Билеты можно приобрести в кассе клуба по цене {price}. "
              "Начало концерта в {start}. \n"
              "Если хотите узнать о концерте в другом городе, "
              "напишите его название. Если хотите закончить "
              "сессию, напишите \"пока\"").format(city=data[1], date=data[2], club=data[3], adress=data[4], price=data[5], start = data[6])))        
    
    with open('concert.pickle', 'wb') as f:
        pickle.dump(answers, f)
        
    with open('photos.pickle', 'rb') as f:
        photos = pickle.load(f)
    photos.update(dict.fromkeys(keys, data[7]))
    with open('photos.pickle', 'wb') as f:
        pickle.dump(photos, f)
        
    with open('cities.pickle', 'rb') as f:
        cities = pickle.load(f)
    if data[0] not in cities:
        cities.append(data[0])
    with open('cities.pickle', 'wb') as f:
        pickle.dump(cities, f)
    
    return "Данные приняты. Можете ввести данные другого концерта или отправить \'@\' для перехода в режим обычного пользователя."
