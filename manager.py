# -*- coding: utf-8 -*-
def greet_manager():
	return ("Здравствуйте, уважаемый менеджер. Если хотите внести информацию "
			"о новом концерте, напишите её в следующем порядке, разделяя "
			"точкой с запятой:\n"
			"город; дата (число цифрами, название месяца словом); название "
			"клуба; адрес клуба; цена билета; время начала концерта. Пример:\n"
			"Москва; 7 января; Punk Fiction; ул. Ольховская, 14с1; 400р; 19:00.\n")
			
def new_gig(data):
	import fileinput
	data = data.replace(' ; ', '_').replace('; ', '_').replace(' ;', '_').replace(';', '_').split('_')
	if len(data) != 6:
		return "всё плохо"
	else:
		replacement_text = """answers[\'{city_lower}\'] = (
    \"Концерт \\"некондиции\\" в г. {city} пройдёт {date} в клубе {club}. \"
    \"Адрес клуба: {adress} \"
    \"Билеты можно приобрести в кассе клуба по цене {price}. \"
    \"Начало концерта в {start}. \\n\"
    \"Если хотите узнать о концерте в другом городе, \"
    \"напишите его название. Если хотите закончить \"
    \"сессию, напишите \\"пока\\"\")
	#append_here""".format(city_lower=data[0].lower(), city=data[0], date=data[1], club=data[2],
		adress=data[3], price=data[4], start = data[5])
		replacement_text.encode('utf-8')
		
		with open('msg.py', 'r', encoding='utf-8') as file:
			filedata = file.read()
		
		filedata = filedata.replace('#append_here', replacement_text)

		with open('msg.py', 'w', encoding='utf-8') as file:
			file.write(filedata)
		return "всё хорошо"
