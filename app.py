import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты>\<в какую валюту перевести>\<количество переводимой валюты>\nУвидить список всех досупных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
        bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
           raise ConvertionException('Количество параметров привысило допустимое, введите /help для уточнения')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Пользователь допустил ошибку.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Команда не была обработана\n{e}')
    else:
        a = float(amount)
        b = float(total_base)
        c = a * b
        c = round(c,2)
        text = f'Стоимость {amount} {quote} в {base} - {c}'
        bot.send_message(message.chat.id, text)

bot.polling()
