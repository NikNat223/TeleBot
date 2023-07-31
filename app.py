import telebot
from key_s import keys
from tokken import TOKEN
from extensions import APIException, ExchangeConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Здравствуйте!\nДля начала работы введите команду в следующем формате: \
\n<наименование валюты цену которой Вы хотите узнать> \
<наименование валюты в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException("Параметров больше, чем нужно.")
        elif len(values) < 3:
            raise APIException("Параметров меньше, чем нужно.")

        base, quote, amount = values
        total_base = ExchangeConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)



