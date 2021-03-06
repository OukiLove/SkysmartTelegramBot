import random
from time import sleep
from telebot import types, telebot, TeleBot
import requests
import asyncio
from Skysmart import answerparse
from datetime import datetime
from os import fspath, mkdir, path

#ur telegram bot token
token = ''
bot = TeleBot(token)

def addToStat(command):
    now = datetime.now()
    # if not folder with name sata then create it
    if not path.exists(f"stat"):
        mkdir("stat")
    filename = f"stat/{now.day}.{now.month}.{now.year}.txt"
    if not fspath(filename):
        with open(filename, "w") as f:
            f.write("")
    with open(filename, "a") as f:
        f.write(command + "\n")

def readDayStat():
    now = datetime.now()
    filename = f"stat/{now.day}.{now.month}.{now.year}.txt"
    linesCount = open(filename, "r").readlines()
    return len(linesCount)

def Skysmart(message):
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
        if message.text.startswith('http'):
            bot.send_message(message.chat.id, text='Такой тип ссылкок не поддерживается')
        else:
            bot.send_message(message.chat.id, text='Это не ссылка')

def RandomRandint(message):
    range = message.text
    if range.isnumeric():
        if int(range) > 0:
            answer = random.randint(1, int(range))
            bot.send_message(message.chat.id, text=answer)
        else:
            bot.send_message(message.chat.id, text='Число равно 0')
    else:
        bot.send_message(message.chat.id, text='Это не число')

def Minigame(message):
        UserNumber = message.text
        if UserNumber.isnumeric():
            if int(UserNumber) > 1 and int(UserNumber) < 10:
                UserNumber = int(UserNumber)
                BotNumber = random.randint(1, 10)
                bot.send_message(message.chat.id, text='Ты выбрал: ' + str(UserNumber))
                bot.send_message(message.chat.id, text='Бот выбрал: ' + str(BotNumber))
                if (UserNumber == BotNumber):
                    bot.send_message(message.chat.id, text='Ты выйграл!')
                else:
                    bot.send_message(message.chat.id, text='Ничего в следующий раз все получится!')
            else:
                bot.send_message(message.chat.id, text='Число меньше 1 или больше 10')
        else:
            bot.send_message(message.chat.id, text='Это не число')

@bot.message_handler(commands=['start'])
def Panel(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Skysmart', 'РЭШ', 'Обновления')
    keyboard.row('Мини игра', 'Погода', 'Генератор чисел')
    button = telebot.types.KeyboardButton(text='Информация')
    keyboard.add(button)
    if message.text == '⒊Назад':
        bot.send_message(message.chat.id, text='Ты вышел из админ панельки', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, text='Привет, выбери функцию', reply_markup=keyboard)

def AdminPanel(message):
    # ⒈ ⒉ ⒊ ⒋ ⒌ ⒍ ⒎ ⒏ ⒐ ⒑ ⒒ ⒓ ⒔ ⒕ ⒖ ⒗ ⒘ ⒙ ⒚ ⒛ Такие числа, потому что люди могут ручками написать, например "Остановить бота" и бот остановится
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⒈Статистика бота', '⒉Остановить бота')
    button = telebot.types.KeyboardButton(text='⒊Назад')
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Ты попал в админ панельку :D', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def ShopaSlona(message):
    if message.text == 'Skysmart':
        addToStat(message.text)
        bot.send_message(message.chat.id, text='Вставте ссылку')
        bot.register_next_step_handler(message, Skysmart)

    if message.text == 'Генератор чисел':
        addToStat(message.text)
        bot.send_message(message.chat.id, text='Введите диапазон чисел')
        bot.register_next_step_handler(message, RandomRandint)

    if message.text == 'РЭШ':
        addToStat(message.text)
        bot.send_message(message.chat.id, text='Расширение для Google Chrome: https://resh.ilsur.dev/')

    if message.text == 'Погода':
        addToStat(message.text)
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
        addToStat(message.text)
        bot.send_message(message.chat.id, text='Бот выбрал число от 1 до 10. Твоя задача угадать')
        bot.register_next_step_handler(message, Minigame)      
    
    if message.text == 'Обновления':
        addToStat(message.text)
        bot.send_message(message.chat.id, text='09.05.22 - Исправлены недоработки')
        bot.send_message(message.chat.id, text='08.05.22 - Добавлен генератор рандомных чисел')
        bot.send_message(message.chat.id, text='05.05.22 - Добавлена поддержка Skysmart (в информации поддерживаемые ссылки)')
        bot.send_message(message.chat.id, text='04.05.22 - Добавлена мини игра')
        bot.send_message(message.chat.id, text='04.05.22 - Добавлена поддержка РЭШ')
        bot.send_message(message.chat.id, text='29.04.22 - Добавлена погода')

    if message.text == 'Информация':
        addToStat(message.text)
        bot.send_message(message.chat.id, text='Разработчики: \n@Ouki76\n@Ded_in_morg')
        bot.send_message(message.chat.id, text='Сайт разработчика:\nhttps://oukilove.github.io/')
        bot.send_message(message.chat.id, text='Исходники телеграмм бота:\nhttps://github.com/OukiLove/SkysmartTelegramBot')
        bot.send_message(message.chat.id, text='Скрипт, который использует бот: https://github.com/xartd0/SKYSMART-ANSWERS')
        bot.send_message(message.chat.id, text='Skysmart поддерживает 2 типа ссылки:\n-https://api-edu.skysmart.ru/api/v1/dnevnikru/homework?taskHash=\n-https://edu.skysmart.ru/student/')      

# -------------------------------------Admin Command---------------------------------------------------------------------------------
    if message.text == 'password':
        AdminPanel(message)

    if message.text == '⒈Статистика бота':
        brawl = readDayStat()
        bot.send_message(message.chat.id, text='Сегодня ботом воспользовались: ' + str(brawl))

    if message.text == '⒉Остановить бота':
        bot.send_message(message.chat.id, text='Бот остановлен')
        bot.stop_bot()
    
    if message.text == '⒊Назад':
        Panel(message)
# -------------------------------------Admin Command---------------------------------------------------------------------------------
bot.polling(non_stop=True)