import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

#команда для показа информации о работе бота
@bot.message_handler(commands=['start', 'help'])
def welcome(message: telebot.types. Message):
    text = f"Добро пожаловать, {message.chat.username}!\n " \
           f"Для начала работы необходимо введите команду в следущем формате:\n " \
           f"<наименование валюты>\n " \
           f"<в какую валюту перевести>\n " \
           f"<количество валюты для конвертации>\n" \
           f"Чтобы увидеть список всех доступных валют введите команду: /values"
    bot.send_message(message.chat.id, text)

#реакция бота на картинки
@bot.message_handler(content_types=['photo'])
def picture(message: telebot.types. Message):
    bot.reply_to(message,  'Красиво, но я картинками не увлекаюсь, попробуй ввести команду /help, чтобы узнать, что я могую')

#реакция бота на аудио сообщение и доки
@bot.message_handler(content_types=['document', 'voice'])
def repeat(message: telebot.types. Message):
    bot.send_message(message.chat.id, 'Ничего не понимаю, попробуй текстом или введи команду /help, чтобы узнать, что я могую')

#команда показывает информацию о доступных валютах
@bot.message_handler(commands=['values'])
def val(message: telebot.types. Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.send_message(message.chat.id, text)

#команда для конвертации
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types. Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя \n {e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')

    else:
        text = f'{amount} {quote} = {round(total_base*float(amount),2)} {base}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)
