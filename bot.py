import telebot
from telebot import types
from utils import get_events, get_me, create_student, update_student, take_part, get_my_events, get_month

TOKEN = "1062715318:AAEHNTnf9YdFnBI8yLH5qCUL27z8wAZfY1A"

bot = telebot.AsyncTeleBot(TOKEN)

csrf_token = ''


@bot.message_handler(commands=['start'])
def send_events(msg):
    """Загрузка мероприятий с сервера"""
    global csrf_token
    data, csrf_token = get_events()

    markup = types.ReplyKeyboardRemove()
    bot.send_message(msg.chat.id, 'Список доступных мероприятий:', reply_markup=markup).wait()

    events = data['data']['events']
    for event in events:
        date_list = event['date'].split('-')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Записаться на мероприятие', callback_data=f'follow_{event["id"]}'))
        bot.send_message(msg.chat.id,
                         f'*{event["name"]}*\n\n{event["description"]}\n\nДата окончания регистрации: ' +
                         f'{date_list[2]} {get_month(int(date_list[1]))}',
                         parse_mode='Markdown',
                         reply_markup=markup
                         ).wait()


@bot.callback_query_handler(func=lambda call: True)
def event_actions(call):
    """Функция-роутер для обработчиков действий, связанных с мероприятиями"""
    if call:
        call_code, call_data = call.data.split('_')
        if call_code == 'follow':
            register(call.message, call_data)


def register(msg, event_id, valid=True):
    """Регистрация на мероприятие"""

    global csrf_token

    if valid and (my_instance := get_me(msg.chat.username, csrf_token)).get('errors') is None:
        me = my_instance['data']['me']
        markup = types.ReplyKeyboardMarkup(row_width=1)
        markup.add(
            types.KeyboardButton('Да, это я'),
            types.KeyboardButton('Нет, хочу поменять данные')
        )
        bot.send_message(msg.chat.id,
                         f'Это вы?\n\n{me["name"]}\n{me["faculty"]} {me["group"]}\n{me["phone"]}',
                         reply_markup=markup
                         ).wait()
    else:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(msg.chat.id, 'Введите ваше ФИО', reply_markup=markup).wait()

    bot.register_next_step_handler(msg, get_name, event_id, valid)


def get_name(msg, event_id, valid):

    if msg.text == 'Да, это я':

        response = take_part(msg.chat.username, event_id, csrf_token)

        markup = types.ReplyKeyboardMarkup()
        markup.add(
            types.KeyboardButton('Показать другие мероприятия'),
            types.KeyboardButton('Показать мои мероприятия')
        )

        if response['data'].get('updateStudent') and response['data'].get('updateStudent')['ok']:
            bot.send_message(msg.chat.id, 'Вы успешно зарегистрированы!', reply_markup=markup).wait()
        else:
            bot.send_message(msg.chat.id, 'Что-то пошло не так', reply_markup=markup).wait()
    elif msg.text == 'Нет, хочу поменять данные':
        register(msg, event_id, False)
    else:
        name = msg.text
        bot.send_message(msg.chat.id, 'Введите ваш факультет в сокращенном виде').wait()
        bot.register_next_step_handler(msg, get_faculty, event_id, name, valid)


def get_faculty(msg, event_id, name, valid):
    faculty = msg.text
    bot.send_message(msg.chat.id, 'Введите вашу группу').wait()
    bot.register_next_step_handler(msg, get_group, event_id, name, faculty, valid)


def get_group(msg, event_id, name, faculty, valid):
    group = msg.text
    bot.send_message(msg.chat.id, 'Введите ваш номер телефона').wait()
    bot.register_next_step_handler(msg, get_phone, event_id, name, faculty, group, valid)


def get_phone(msg, event_id, name, faculty, group, valid):

    phone = msg.text
    if valid:
        response = create_student(msg.chat.username, name,
                                  faculty, group, phone,
                                  event_id, csrf_token)
    else:
        response = update_student(msg.chat.username, name,
                                  faculty, group, phone, csrf_token)

    markup = types.ReplyKeyboardMarkup()
    markup.add(
        types.KeyboardButton('Показать другие мероприятия'),
        types.KeyboardButton('Показать мои мероприятия')
    )

    if response['data'].get('createStudent') and response['data'].get('createStudent')['ok']:
        bot.send_message(msg.chat.id, 'Вы успешно зарегистрированы!', reply_markup=markup).wait()
    elif response['data'].get('updateStudent') and response['data'].get('updateStudent')['ok']:
        bot.send_message(msg.chat.id, 'Ваши данные успешно обновлены!').wait()
        response = take_part(msg.chat.username, event_id, csrf_token)
        if response['data'].get('updateStudent') and response['data'].get('updateStudent')['ok']:
            bot.send_message(msg.chat.id, 'Вы успешно зарегистрированы!', reply_markup=markup).wait()
        else:
            bot.send_message(msg.chat.id, 'Что-то пошло не так', reply_markup=markup).wait()
    else:
        bot.send_message(msg.chat.id, 'Что-то пошло не так', reply_markup=markup).wait()


@bot.message_handler(func=lambda msg: msg.text == 'Показать другие мероприятия')
def show_events(msg):

    markup = types.ReplyKeyboardRemove()
    bot.send_message(msg.chat.id, '', reply_markup=markup).wait()
    send_events(msg)


@bot.message_handler(func=lambda msg: msg.text == 'Показать мои мероприятия')
def show_my_events(msg):
    data = get_my_events(msg.chat.username)

    events = data['data']['myEvents']
    for event in events:
        bot.send_message(msg.chat.id,
                         f'*{event["name"]}*\n\n{event["description"]}',
                         parse_mode='Markdown'
                         ).wait()


def get_full_information(msg, event_id):
    """Получение подробной информации о мероприятии"""
    pass


if __name__ == "__main__":
    bot.polling()
