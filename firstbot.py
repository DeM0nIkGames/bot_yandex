import telebot


bot = telebot.TeleBot("6206338407:AAEaSdTOIDMLMxSYsOH0SRjyEyFJh6aOu0o")


@bot.message_handler(content_types=['text'])
def main_cycle(message):
    if message.text == '/info':
        bot.send_message(message.from_user.id, "Напишите /info")
    else:
        bot.send_message(message.from_user.id, "Наши боты:")
        bot.send_message(message.from_user.id, "Бот для заметок - @MinionBananaBot")
        bot.send_message(message.from_user.id, "Бот для тайм-менеджмента - t.me/time111bot")


bot.polling(none_stop=True, interval=0)