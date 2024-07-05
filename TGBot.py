import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду в следующем формате:\n<Имя валюты> <В какую валюту перевести> <Количество валюты>\nЧтобы узнать доступные валюты, введите команду /values"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException("Неверное количество параметров")

        base, quote, amount = values
        total = CurrencyConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {base} в {quote} - {total['result']}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

