from functions.phone import check_phone
import time
from models import *
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
import requests
import settings
import json
import datetime


###### ###### ###### // Permissions \\ ###### ######  ######


###### ###### ###### \\ Permissions // ###### ######  ######



###### ###### ###### // Bot returns \\ ###### ######  ######

def send_message(chat_id, text):
    send_result = requests.get(
        f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage',
        params={'chat_id': chat_id, 'text': text})

###### ###### ###### \\ Bot returns // ###### ######  ######



###### ###### ###### // DB searching \\ ###### ######  ######

def checkUser(telegram_id):
	with Session(bind=engine) as db:
	    query = db.query(User).filter(User.telegram_id == telegram_id).first()
	    if query is not None:
	    	return True
	    else: return False

def getPhoneOperator(code):
	with Session(bind=engine) as db:
		query = db.query(Operator).filter(Operator.code == code).first()
		if query is not None:
			return query.name
		else: return False


def getScammer(phone):
	with Session(bind=engine) as db:
		queryset = db.query(Scammer).filter(Scammer.phone == phone)
		groups = [None]
		for query in queryset:
			if query.group not in groups:
				groups[0] = True
				groups.append(query.group)
		if groups[0] != None:
			return groups[1:]
		else: 
			return False


def findForPhone(phone):
	with Session(bind=engine) as db:
		query = db.query(Uncap).filter(Uncap.phone == phone).first()
		return query

###### ###### ###### \\ DB searching // ###### ######  ######



###### ###### ###### // Checkings \\ ###### ######  ######


def renderDate(date):
	date = datetime.datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')


def checkWP(phone):
	# url = f"https://api.green-api.com/waInstance{settings.GREEN_INSTANCE}/checkWhatsapp/{settings.GREEN_TOKEN}"
	# payload = json.dumps({ "phoneNumber": phone[1:] })
	# headers = {'Content-Type': 'application/json'}
	# response = requests.request("POST", url, headers=headers, data = payload)
	# return json.loads(response.text)['existsWhatsapp']
	return True

###### ###### ###### \\ Checkings // ###### ######  ######



###### ###### ###### // Message building \\ ###### ######  ######

def composeMessage(chat_id, user_id, user_name, key, check):
	plusSearch(user_id)
	saveSearcher(telegram_id=user_id, search=check, user_name=user_name, key='phone')
	baseInfo = findForPhone(check)
	scammer = getScammer(check)
	if checkWP(check) is True:
		WP_status = '✅'
	else : WP_status = '❌'

	message = '🕵️ Найденая информация по номеру '+check+' :\n\n'
	if baseInfo is not None:

		if baseInfo.name is not None:
			name = baseInfo.name
			message = message+'🙈  Имя: '+name+'\n\n'

			social_media = search_in_google(name)
			if len(social_media) > 0:
				message = message+'🔎  Это имя в гугле ↙️'+'\n\n'
			for sc in social_media:
				message = message+'   '+social_media[sc]+'\n\n'

		if baseInfo.city is not None:
			city = baseInfo.city
			message = message+'🏘  Город: '+city+'\n\n'
		if baseInfo.email is not None:
			email = baseInfo.email
			message = message+'📩  Email: '+email+'\n\n'
		if baseInfo.birthday is not None:
			birthday = baseInfo.birthday
			message = message+'🎂  День рождения: '+birthday+'\n\n'

	operator = getPhoneOperator(check[:5])
	if operator is not False:
		message = message+'Страна: Казахстан 🇰🇿 \n\n'
		message = message+'🌐  Оператор: '+operator+'\n\n'

	if scammer is not False:
		for s in scammer:
			message = message+'👺  Найден в базе: '+s+'\n\n'
	message = message+'💬  WhatsApp: '+WP_status+'\n\n'

	send_message(chat_id, message)


def getInfoByIIN(IIN):
	url = f"https://pk.uchet.kz/p/iin/{IIN}/full/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "html.parser")
	info = []
	if 'info-value col' in page.text:
		
		for block in soup.find_all('div', class_='info-value col'):
			if block.text.replace('\n', '') != 'Нет':
				info.append(block.text.replace('\n', ''))
			else:
				continue

		text = '🕵️ Найденая информация по ИИНу:\n\n'
		for t in info:
			text += t+"\n\n"
		return text

	else : return '😔 Информация по ИИНу не найдена.'

###### ###### ###### \\ Message building // ###### ######  ######


###### ###### ###### // Others SQL \\ ###### ######  ######

def saveUser(telegram_id, name, chat_id):
	if checkUser(telegram_id):
		message = f'С возвращением, наш друг! 🎉'
		send_message(chat_id, message)
	else:
		with Session(bind=engine) as db:
		    user = User(telegram_id=telegram_id, name=name)
		    db.add(user)
		    db.commit()

		message = 'Добро пожаловать!\nОтправте нам намер телефона.'
		send_message(chat_id, message) 


def getUser(telegram_id):
	with Session(bind=engine) as db:
		user = db.query(User).filter(User.telegram_id == telegram_id)
		return user

def plusSearch(telegram_id):
	with Session(bind=engine) as db:
		user = db.query(User).filter(User.telegram_id == telegram_id).first()
		user.search_count += 1
		db.add(user)
		db.commit()


def saveSearcher(telegram_id, user_name, search, key):
	if key == 'phone':
		with Session(bind=engine) as db:
		    user = Searcher(telegram_id=telegram_id, wh_phone_search=search, name=user_name)
		    db.add(user)
		    db.commit()
	elif key == 'command':
		with Session(bind=engine) as db:
		    user = Searcher(telegram_id=telegram_id, wh_command_search=search, name=user_name)
		    db.add(user)
		    db.commit()

###### ###### ###### \\ Others SQL // ###### ######  ######


def search_in_google(name):
	words = name.split(' ')
	if len(words)>2:
		name = " ".join(words[:2])
	url = f'https://www.google.com/search?q={name}'
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "html.parser")
	data = {}
	for block in soup.find_all('div', class_='Gx5Zad fP1Qef xpd EtOod pkphOe'):
		link = block.find('a').get('href').replace('/url?q=https://', '')
		if 'vk.com' in link and 'topic' not in link:
			words = link.split('/')
			for el in words:
				if '&' in el:
					index = el.index('&')
					profile = el[:index]
					data['vk.com'] = f'www.vk.com/{profile}'
		if 'ok.ru/profile/' in link:
			words = link.split('/')
			profile = words[words.index('profile')+1].split('&')[0]
			data['ok.ru'] = f'www.ok.ru/profile/{profile}'
	return data










