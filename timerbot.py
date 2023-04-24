import telebot
from telebot import types
import sqlite3
import datetime
import time as tt
# Bot Timer
# Key1 - Посмотреть все записи и их периодичность
# Key2 - Сделать новую запись
# Key3 - Удалить запись
# Key4 - Настроить существующую запись
# В частоте:
# 0 - не повторять
# 1 - повторять каждый день
# 2 - повторять каждую неделю
db = sqlite3.connect('messages', check_same_thread=False)
days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
bot = telebot.TeleBot('5993527558:AAGp49CGPPjmGK1i37dpFGpWImmaS4gXnxs')
timetables = {}
frequency = {}
for i in range(24):
    for j in range(60):
        if len(str(i)) == 1:
            i = '0' + str(i)
        if len(str(j)) == 1:
            j = '0' + str(j)
        time = str(i) + ':' + str(j)
        timetables[time] = ''
        frequency[time] = 0


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "0":
        sender = str(call.message.chat.id)
        cur = db.cursor()
        cur.execute("""INSERT INTO users (sender, time, day, event, frequency) VALUES (?, ?, ?, ?, ?)""", (sender, time, day, event, '0'))
        db.commit()
        bot.send_message(call.message.chat.id, 'Сделано!')
    elif call.data == "1":
        sender = str(call.message.chat.id)
        cur = db.cursor()
        cur.execute("""INSERT INTO users (sender, time, day, event, frequency) VALUES (?, ?, ?, ?, ?)""", (sender, time, day, event, '1'))
        db.commit()
        bot.send_message(call.message.chat.id, 'Сделано!')
    elif call.data == "2":
        sender = str(call.message.chat.id)
        cur = db.cursor()
        cur.execute("""INSERT INTO users (sender, time, day, event, frequency) VALUES (?, ?, ?, ?, ?)""", (sender, time, day, event, '2'))
        db.commit()
        bot.send_message(call.message.chat.id, 'Сделано!')


# Создание
def get_creating(message):
    global time
    time = message.text
    if time.count(':') == 1:
        hours, minutes = time.split(':')
        try:
            hours, minutes = int(hours), int(minutes)
            if hours < 24 and minutes < 60 and 1 <= len(str(hours)) <= 2 and (len(str(minutes)) == 2 or minutes == 0):
                if hours < 10:
                    hours = '0' + str(hours)
                if minutes == 0:
                    minutes = str(minutes) * 2
            else:
                return False
            cur = db.cursor()
            time = str(hours) + ':' + str(minutes)
            sender = str(message.from_user.id)
            if cur.execute("""SELECT * FROM users WHERE sender like ? AND time like ?""", (sender, time)).fetchall():
                bot.send_message(message.from_user.id, 'Это время уже занято!')
            else:
                bot.send_message(message.from_user.id, 'Что это за событие?')
                bot.register_next_step_handler(message, get_event)
        except ValueError:
            bot.send_message(message.from_user.id, 'Неверный формат. Попробуйте ещё раз')
    else:
        bot.send_message(message.from_user.id, 'Неверный формат. Попробуйте ещё раз')


def get_event(message):
    global event
    event = message.text
    bot.send_message(message.from_user.id, 'В какой день недели мне напомнить?')
    bot.register_next_step_handler(message, get_day)


def get_day(message):
    global day
    day = days.index(message.text.lower())
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Никогда', callback_data='0')
    keyboard.add(key_1)
    key_2 = types.InlineKeyboardButton(text='Каждый день', callback_data='1')
    keyboard.add(key_2)
    key_3 = types.InlineKeyboardButton(text='Каждую неделю', callback_data='2')
    keyboard.add(key_3)
    bot.send_message(message.from_user.id, 'Как часто мне напоминать Вам об этом?', reply_markup=keyboard)


# Удаление
def get_deleting(message):
    time = message.text
    if time.count(':') == 1:
        hours, minutes = time.split(':')
        try:
            hours, minutes = int(hours), int(minutes)
            if hours < 24 and minutes < 60 and 1 <= len(str(hours)) <= 2 and len(str(minutes)) == 2:
                if hours < 10:
                    hours = '0' + str(hours)
            if minutes == 0:
                minutes = '0' + str(minutes)
            cur = db.cursor()
            time = str(hours) + ':' + str(minutes)
            sender = str(message.from_user.id)
            print(cur.execute("""SELECT * FROM users WHERE sender like ? AND time like ?""", (sender, time)).fetchall(), (sender, time))
            if cur.execute("""SELECT * FROM users WHERE sender like ? AND time like ?""", (sender, time)).fetchall():
                bot.send_message(message.from_user.id, 'Удаляю...')
                cur = db.cursor()
                cur.execute("""DELETE FROM users WHERE sender like ? AND time like ?""", (sender, time))
                db.commit()
            else:
                bot.send_message(message.from_user.id, 'Это место уже пусто')
        except ValueError:
            bot.send_message(message.from_user.id, 'Неверный формат. Попробуйте ещё раз')
    else:
        bot.send_message(message.from_user.id, 'Неверный формат. Попробуйте ещё раз')


# Настройка
def get_editing(message):
    global time
    global day
    global event
    time = message.text
    if time.count(':') == 1:
        hours, minutes = time.split(':')
        try:
            hours, minutes = int(hours), int(minutes)
            if hours < 24 and minutes < 60 and 1 <= len(str(hours)) <= 2 and len(str(minutes)) == 2:
                if hours < 10:
                    hours = '0' + str(hours)
            else:
                return False
            time = str(hours) + ':' + str(minutes)
            bot.send_message(message.from_user.id, 'Введите желаемое событие')
            bot.register_next_step_handler(message, get_event)
        except ValueError:
            bot.send_message(message.from_user.id, 'Неверный формат. Попробуйте ещё раз')
    else:
        bot.send_message(message.from_user.id, 'Неверный формат. Попробуйте ещё раз')


# Главный обработчик
@bot.message_handler(content_types=['text'])
def main_cycle(message):
    if message.text == '/info':
        bot.send_message(message.from_user.id, "Здравствуйте, я бот, помогающий людям планировать своё время. Что вы хотели бы сделать? 1 - Посмотреть все записи и их периодичность, 2 - Сделать новую запись, 3 - Удалить запись 4 - Настроить существующую запись")
    elif message.text == "1":
        sender = str(message.from_user.id)
        cur = db.cursor()
        if cur.execute("""SELECT * FROM users where sender like ?""", (sender, )).fetchall():
            arr = cur.execute("""SELECT * FROM users where sender like ?""", (sender, ))
            for el in arr:
                if el[3] == '0':
                    bot.send_message(int(sender), f'{days[el[2]].capitalize()}: В {el[1]} у Вас запланировано событие "{el[3]}". Я напоминаю о нём один раз')
                elif el[3] == '1':
                    bot.send_message(int(sender), f'{days[el[2]].capitalize()}: В {el[1]} у Вас запланировано событие "{el[3]}". Я напоминаю о нём каждый день')
                else:
                    bot.send_message(int(sender), f'{days[el[2]].capitalize()}: В {el[1]} у Вас запланировано событие "{el[3]}". Я напоминаю о нём каждую неделю')
        else:
            bot.send_message(message.from_user.id, 'У вас ещё ничего не запланировано!')
    elif message.text == '2':
        bot.send_message(message.from_user.id, 'В какое время вы хотите создать событие?')
        bot.register_next_step_handler(message, get_creating)
    elif message.text == '3':
        bot.send_message(message.from_user.id, 'Все ваши события:')
        sender = str(message.from_user.id)
        cur = db.cursor()
        arr = cur.execute("""SELECT * FROM users where sender like ?""", (sender, ))
        if not arr:
            bot.send_message(message.from_user.id, 'У вас ещё ничего не запланировано!')
        else:
            for el in arr:
                if el[3] == '0':
                    bot.send_message(int(sender), f'{days[el[2]].capitalize()}: В {el[1]} у Вас запланировано событие "{el[3]}". Я напоминаю о нём один раз')
                elif el[3] == '1':
                    bot.send_message(int(sender), f'{days[el[2]].capitalize()}: В {el[1]} у Вас запланировано событие "{el[3]}". Я напоминаю о нём каждый день')
                else:
                    bot.send_message(int(sender), f'{days[el[2]].capitalize()}: В {el[1]} у Вас запланировано событие "{el[3]}". Я напоминаю о нём каждую неделю')
        bot.send_message(message.from_user.id, 'В какое время вы хотите удалить событие?')
        bot.register_next_step_handler(message, get_deleting)
    elif message.text == '4':
        bot.send_message(message.from_user.id, 'Все ваши события:')
        sender = str(message.from_user.id)
        cur = db.cursor()
        arr = cur.execute("""SELECT * FROM users where sender like ?""", (sender, ))
        if not arr:
            bot.send_message(message.from_user.id, 'У вас ещё ничего не запланировано!')
        else:
            for el in arr:
                if el[3] == '0':
                    bot.send_message(int(sender), f'{days[el[2]].capitalize()}: В {el[1]} у Вас запланировано событие "{el[3]}". Я напоминаю о нём один раз')
                elif el[3] == '1':
                    bot.send_message(int(sender), f'{days[el[2]].capitalize()}: В {el[1]} у Вас запланировано событие "{el[3]}". Я напоминаю о нём каждый день')
                else:
                    bot.send_message(int(sender), f'{days[el[2]].capitalize()}: В {el[1]} у Вас запланировано событие "{el[3]}". Я напоминаю о нём каждую неделю')
        bot.send_message(message.from_user.id, 'В какое время вы хотите изменить событие?')
        bot.register_next_step_handler(message, get_editing)
    else:
        bot.send_message(message.from_user.id, 'Напишите /info для начала')


# Главный цикл
def main():
    bot.polling(none_stop=True, interval=0)
    while True:
        c = 0
        while c < 10000:
            c += 1
        if str(datetime.datetime.now().second) == '0':
            cur = db.cursor()
            arr = cur.execute("""SELECT * FROM users""").fetchall()
            for el in arr:
                sender, t, d, ev, fr = el
                if t == (str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute)):
                    if fr == '1':
                        bot.send_message(int(sender), f'Доброго времени суток! Напоминаю Вам о событии "{ev}"')
                    elif d == datetime.datetime.now().weekday():
                        bot.send_message(int(sender), f'Доброго времени суток! Напоминаю Вам о событии "{ev}"')
                        if fr == '0':
                            cur.execute(
                                """DELETE FROM users WHERE sender like ? AND time like ? AND day like ? AND event like ? AND frequency like ?""",
                                (sender, t, d, ev, fr))
                            db.commit()


if __name__ == '__main__':
    main()
