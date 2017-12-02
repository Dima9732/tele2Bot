import telebot.types as types

def generate_markup(file):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param file: файл с описанием кнопок
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    with open(file) as f:
        li = f.read().split('\n')

    for item in li:
        markup.add(item)

    return markup


