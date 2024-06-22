#import libraries
import telebot
from datetime import datetime

start_time = datetime.now()

#get api key
def get_config(dir):
    api_key = ""
    with open(dir, "r") as config_file:
        api_key = config_file.read()
    return api_key

#declare bot object
bot = telebot.TeleBot(get_config("config.ini"))

#starting
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text == "/help" or message.text == "/start":
	    bot.send_message(message.chat.id, "Добрый день! Бот запущен в " + start_time.strftime("%d.%m.%Y %H:%M:%S"))

#get message
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "бот":
        bot.send_message(message.chat.id, "Добрый день! Бот работает с " + start_time.strftime("%d.%m.%Y %H:%M:%S"))
    #write message text in the end of file
    print(message.text)
    with open(log_filename, "a") as log:
        log.write("\n" + message.text + "\n========")

#open or create file to store messages
log_filename = "log_" + datetime.now().strftime("%d_%m_%Y__%H_%M_%S") + ".txt"

bot.polling(none_stop=True, interval=0)