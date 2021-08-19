import telebot
from config import keys, TOKEN, help_text
from extensions import ConvertException, CurrencyConvertor

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в виде: \
    \n<имя первой валюты> \
    \n<имя второй валюты> \
    \n<сумма в первой валюте> \
    \nНапример: 35 доллар рубль \
    \n \
    \n Список доступных валют - команда: \
    \n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message, text + '\n' + help_text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message): 

    try: 
        values = message.text.split(' ')

        if len(values) != 3: 
            raise ConvertException(f'Неверно заданы аргументы. \
                {help_text}')

        amount, base, quote = values
        get_quote = CurrencyConvertor.convert(quote, base, amount)

    except ConvertException as e:
        bot.reply_to(message, f'Ошибка ввода: \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не могу выполнить команду: \n{e} \
            {help_text}')

    else: 
        converted = round(float(get_quote) * float(amount), 2)
        text = f'{amount} {keys[base]} = {converted} {keys[quote]}.'
        bot.send_message(message.chat.id, text)

bot.polling()