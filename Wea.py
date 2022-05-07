from asyncio.windows_events import NULL
import random
from time import sleep
from telebot import types, telebot, TeleBot
import requests
import asyncio
from Skysmart import answerparse

#ur telegram bot token
token = ''
bot = TeleBot(token)

def Dadada(message):
    if message.text.startswith('https://api-edu.skysmart.ru/api/v1/dnevnikru/homework?taskHash=') or message.text.startswith('https://edu.skysmart.ru/student/'):
        UserInput = message.text
        if message.text.startswith('https://edu.skysmart.ru/student/'):
            Room = UserInput.split('https://edu.skysmart.ru/student/')
        else:
            Room = UserInput.split('https://api-edu.skysmart.ru/api/v1/dnevnikru/homework?taskHash=')
        JoinRoom = ''.join(Room)
        bot.send_message(message.chat.id, text=JoinRoom)
        loop = asyncio.new_event_loop()
        Answer = loop.run_until_complete(answerparse(taskHash=JoinRoom))
        JoinAnswer = '\n'.join(Answer)
        loop.close()
        otv = JoinAnswer.split('`')
        for i in range(len(otv)):
            if otv[i] != '':
                bot.send_message(message.chat.id, text=otv[i])
    else:
        bot.send_message(message.chat.id, text='Это не ссылка!')

def Bomber(message):
    UserInput = message.text
    if message.text.startswith('+'):
        2 + 2
    else:
        bot.send_message(message.chat.id, text='Начните вводить телефон с "+"')


def Minigame(message):
        UserNumber = message.text
        if UserNumber.isnumeric():
            UserNumber = int(UserNumber)
            BotNumber = random.randint(1, 10)
            bot.send_message(message.chat.id, text='Ты выбрал: ' + str(UserNumber))
            bot.send_message(message.chat.id, text='Бот выбрал: ' + str(BotNumber))
            if (UserNumber == BotNumber):
                    bot.send_message(message.chat.id, text='Ты выйграл!')
            else:
                bot.send_message(message.chat.id, text='Ничего в следующий раз все получится!')
        else:
            bot.send_message(message.chat.id, text='Это не число')
            bot.send_message(message.chat.id, text='Введи число от 1 до 10')
#            bot.register_next_step_handler(message, Minigame) лучше убрать, потому что если пользователь случайно нажал на Minigame, он будет вынужден ввести число

@bot.message_handler(commands=['start'])
def Panel(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Skysmart', 'РЭШ', 'Погода', 'Обновления', 'Мини игра')
    button = telebot.types.KeyboardButton(text='Информация')
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Привет, выбери функцию', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def ShopaSlona(message):
    if message.text == 'Skysmart':
        bot.send_message(message.chat.id, text='Вставте ссылку')
        bot.register_next_step_handler(message, Dadada)

    if message.text == 'РЭШ':
        bot.send_message(message.chat.id, text='Расширение для Google Chrome: https://resh.ilsur.dev/')
    
    if message.text == 'Я гей':
        bot.send_message(message.chat.id, text='Нашел пасхалку, но бот остановиться навсегда :DDD')
        bot.stop_bot()

    if message.text == 'Погода':
        city = 'Omsk,RU'
        city_id = 1496153
        appid = '6abf7fd9e585da77f917619a30194935'
        try:
                res = requests.get('http://api.openweathermap.org/data/2.5/weather', params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                data = res.json()
                temp = data['main']['temp']
                temp_min = data['main']['temp_min']
                temp_max = data['main']['temp_max']
                bot.send_message(message.chat.id, text= city)
                bot.send_message(message.chat.id, text= 'Temp now: ' + str(temp) + '°C')
                bot.send_message(message.chat.id, text= 'Temp min: ' + str(temp_min) + '°C')
                bot.send_message(message.chat.id, text= 'Temp max: ' + str(temp_max) + '°C')

        except Exception as e:
                bot.send_message(message.chat.id, text = e)
                pass

    if message.text == 'Мини игра':
        bot.send_message(message.chat.id, text='Бот выбрал число от 1 до 10. Твоя задача угадать')
        bot.register_next_step_handler(message, Minigame)      
    
    if message.text == ('Обновления'):
        bot.send_message(message.chat.id, text='05.05.22 - Добавлена поддержка Skysmart (в информации поддерживаемые ссылки)')
        bot.send_message(message.chat.id, text='04.05.22 - Добавлена мини игра')
        bot.send_message(message.chat.id, text='04.05.22 - Добавлена поддержка РЭШ')
        bot.send_message(message.chat.id, text='30.04.22 - Добавлена минимальная и максимальная температура')
        bot.send_message(message.chat.id, text='29.04.22 - Добавлена погода')
        bot.send_message(message.chat.id, text='29.04.22 - Добавлены кнопки снизу')

    if message.text == ('Информация'):
        bot.send_message(message.chat.id, text='Разработчики: \n@Ouki76\n@Ded_in_morg')
        bot.send_message(message.chat.id, text='Skysmart поддерживает 2 типа ссылки:\n-https://api-edu.skysmart.ru/api/v1/dnevnikru/homework?taskHash=\n-https://edu.skysmart.ru/student/')
        bot.send_message(message.chat.id, text='Скрипт, который использует бот: https://github.com/xartd0/SKYSMART-ANSWERS')
            
bot.polling(non_stop=True)