def checknum(s):
	s.replace(' ', '')
	result = "7"
	if s[0] in ('+', '7', '8'):
		if s[0] == '+':
			if s[1] in('7', '8'):
				if len(s) < 12:
					print('В вашем номере недостаточно цифр. Попробуйте снова.\nПример: 79030001122')
					return
				elif len(s) > 12:
					print('В вашем номере многовато цифр. Попробуйте снова.')
					return
				else:
					result += s[2:]
			else:
				print('Ваш номер должен начинаться на +, 7 или 8')
				return
		else:
			if len(s) > 11:
				print('В вашем номере многовато цифр. Попробуйте снова.')
				return
			elif len(s) < 11:
				print('В вашем номере недостаточно цифр. Попробуйте снова.')
				return
			else:
				result += s[1:]
	else:
		print('Обратите внимание на формат ввода номера.\nВвод начинается с 7. Пример: 79030001122')
		return
	print('Успешненько')
	return result