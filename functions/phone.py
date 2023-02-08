def check_phone(phone):
	try:
		if phone is None:
			return None
		elif len(phone) == 12 and phone[0] == '+':
			if ' ' in phone:
				return check_phone(phone.replace(' ', ''))
			return phone
		elif len(phone) == 11:
			if phone[0] == '8':
				phone = '+7'+phone[1:]
				return phone
			elif phone[0] == '+':
				phone = '+7'+phone[1:]
				return phone
			else: 
				phone = '+'+phone
				return phone
		elif len(phone) == 10:
			phone = '+7'+phone
			return phone
		elif len(phone) == 9:
			phone = '+77'+phone
			return phone
		elif ' ' in phone:
			return check_phone(phone.replace(' ', ''))
		elif ' ' in phone:
			return check_phone(phone.replace(' ', ''))
		elif '-' in phone:
			return check_phone(phone.replace('-', ''))
		elif '–' in phone:
			return check_phone(phone.replace('–', ''))
		elif '(' or ')' in phone:
			return check_phone(phone.replace('(', '').replace(')', ''))
		else:
			print(f'{phone} - is not deformed!')	
			return None
	except RecursionError:
		return None









