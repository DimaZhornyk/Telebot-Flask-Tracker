from telebot import types, apihelper
import time
import telebot
from database import Locations, Workers, History, db

bot = telebot.TeleBot('973520242:AAH8WeGRmUNqKzYDdM1PCURHoojkNYWATwU')

# apihelper.proxy = {'https': 'socks5://403316002:uRRAwCvc@grsst.s5.opennetwork.cc:999'}
globaltime = {}


def count_locations():
    return Locations.count_documents({})


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет, я ваш бот. Я умею считать ваше рабочее время и показывать накопленные часы. "
                     "Делаю я это только если вы находтесь на рабочем месте. Для начала работы, нажмите /go")


@bot.message_handler(commands=['go'])
def name_listener(message):
    try:
        outname = Workers.find_one({"Telegram": message.chat.id})
    except:
        outname = None
    if outname:
        bot.send_message(message.chat.id, '''Вы находитесь в главном меню. Доступные вам команды:
        		/begin для начала отсчета
        		/stop для окончания отсчета
        		/time для отображения накопленного времени''')
        bot.register_next_step_handler(message, free_time_function)
    else:
        bot.send_message(message.chat.id, 'Введите свое имя')
        bot.register_next_step_handler(message, surname_listener)


def surname_listener(message):
    Workers.insert_one({"Telegram": message.chat.id,
                        "Name": message.text,
                        "Surname": "",
                        "Total time": "0:0:0",
                        "Last project": "",
                        "Last job": "",
                        "Last lat": 0,
                        "Last lng": 0
                        })
    bot.send_message(message.chat.id, 'Введите свою фамилию')
    bot.register_next_step_handler(message, surname_handler)


def surname_handler(message):
    Workers.update_one({"Telegram": message.chat.id}, {"$set": {"Surname": message.text}})
    bot.send_message(message.chat.id, '''Регистрация прошла успешно, тепер вы можете использовать бота. Его команды:
        /begin для начала отсчета
        /stop для окончания отсчета
        /time для отображения накопленного времени''')


def project_choice(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    locations = [c['Name'] for c in db['Locations'].find()]
    for i in range(0, count_locations()):
        markup.add(types.KeyboardButton(text=locations[i]))
    bot.send_message(message.chat.id, text='Выберите обьект на котором вы работаете:', reply_markup=markup)
    bot.register_next_step_handler(message, geo)


def geo(message):
    try:
        proj_ident = Locations.find_one({"Name": message.text})['_id']
    except Exception as e:
        proj_ident = None
    if proj_ident:
        Workers.update_one({"Telegram": message.chat.id}, {"$set": {"Last project": proj_ident}})
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id,
                         "Нажмите на кнопку и передайте мне свое местоположение или нажмите /back для возврата в главное меню",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, location_new)

    else:
        bot.send_message(message.chat.id, "Некорректный ввод")
        bot.register_next_step_handler(message, geo)


def location_new(message):
    proj_ident = Workers.find_one({"Telegram": message.chat.id})["Last project"]
    if message.location:
        latitude_from_base = Locations.find_one({"_id": proj_ident})['Latitude']
        longitude_from_base = Locations.find_one({"_id": proj_ident})['Longitude']

        if latitude_from_base - 0.0035 < message.location.latitude < latitude_from_base + 0.0035 and \
                longitude_from_base - 0.0035 < message.location.longitude < longitude_from_base + 0.0035:
            now = time.time()
            globaltime[message.chat.id] = now
            bot.send_message(message.chat.id,
                             "Ваша локация соответствует необходимой, счетчик запущен. Для его остановки нажмите /stop  ")
            Workers.update_one({"Telegram": message.chat.id}, {"$set": {"Last project": proj_ident}})
            bot.register_next_step_handler(message, stop_function)
        else:
            bot.send_message(message.chat.id,
                             "Ваша геолокация не соответствует необходимой, вернитесь и отправьте геолокацию заново или нажмите /back для возврата в главное меню ")
            bot.register_next_step_handler(message, location_new)
    elif message.text == "/back":
        bot.send_message(message.chat.id, '''Вы находитесь в главном меню. Доступные вам команды:
        		/begin для начала отсчета
        		/stop для окончания отсчета
        		/time для отображения накопленного времени''')
    else:
        bot.send_message(message.chat.id, 'Я ожидаю вашу геолокацию')
        bot.register_next_step_handler(message, location_new)


def stop_function(message):
    if message.text == '/stop':
        bot.send_message(message.chat.id, "Что вы делали сегодня? ")
        bot.register_next_step_handler(message, location_caller)
    else:
        bot.send_message(message.chat.id,
                         "Сейчас вам доступна только команда /stop ")
        bot.register_next_step_handler(message, stop_function)


def location_caller(message):
    if message.text is None:
        bot.send_message(message.chat.id, "Некорректный ввод")
        bot.register_next_step_handler(message, location_caller)
    else:
        Workers.update_one({"Telegram": message.chat.id}, {"$set": {"Last job": message.text}})
        bot.send_message(message.chat.id, "Теперь повторно отправьте свою геолокацию чтобы остановить таймер")
        bot.register_next_step_handler(message, location_stopper)


def location_stopper(message):
    if message.location:
        user_dict = Workers.find_one({"Telegram": message.chat.id})
        lastproject_from_base = user_dict['Last project']

        latitude_from_base = Locations.find_one({"_id": lastproject_from_base})['Latitude']

        longitude_from_base = Locations.find_one({"_id": lastproject_from_base})['Longitude']

        name_from_base = user_dict['Name']

        surname_from_base = user_dict['Surname']

        last_job_from_base = user_dict['Last job']

        last_project_name_from_base = Locations.find_one({"_id": lastproject_from_base})['Name']

        if latitude_from_base - 0.0035 < message.location.latitude < latitude_from_base + 0.0035 and \
                longitude_from_base - 0.0035 < message.location.longitude < longitude_from_base + 0.0035:
            bot.send_message(message.chat.id, "Ваша локация соответствует необходимой, таймер остановлен корректно")
            minutes = 0
            hours = 0
            prev_time = globaltime[message.chat.id]
            now = time.time()
            seconds = int(now - prev_time)
            if seconds >= 60:
                minutes = seconds // 60
                seconds = seconds % 60
            if minutes >= 60:
                hours = minutes // 60
                minutes = minutes % 60

            Workers.update_one({"Telegram": message.chat.id},
                               {"$set": {"Last lat": message.location.latitude,
                                         "Last lng": message.location.longitude}})
            time_list = user_dict['Total time'].split(":")
            hours_from_base = int(time_list[0])

            minutes_from_base = int(time_list[1])

            seconds_from_base = int(time_list[2])

            full_hours = hours + hours_from_base
            full_minutes = minutes + minutes_from_base
            full_secounds = seconds + seconds_from_base
            if full_secounds >= 60:
                full_minutes = full_minutes + (full_secounds // 60)
                full_secounds = full_secounds % 60
            if full_minutes >= 60:
                full_hours = full_hours + (full_minutes // 60)
                full_minutes = full_minutes % 60
            time_totally = str(full_hours) + ":" + str(full_minutes) + ":" + str(full_secounds)
            Workers.update_one({"Telegram": message.chat.id},
                               {"$set": {"Total time": time_totally}})
            fresh_time = str(hours) + ":" + str(minutes) + ":" + str(seconds)
            History.insert_one(
                {"Telegram": message.chat.id, "Name": name_from_base, "Surname": surname_from_base,
                 "Time written": fresh_time, "Time": time.time(),
                 "Project": last_project_name_from_base, "Work": last_job_from_base, "Correct": True})
            bot.send_message(message.chat.id,
                             "За сегодня вы получили {0} часов {1} минут {2} секунд, делая {3} на обьекте  {4}".format(
                                 hours, minutes, seconds, last_job_from_base, last_project_name_from_base))
            bot.send_message(message.chat.id,
                             "Ваше общее время: {0} часов , {1} минут , {2} секунд".format(full_hours, full_minutes,
                                                                                           full_secounds))
            bot.send_message(403316002,
                             "Пользователь {0} {1} остановил таймер корректно, начав работу на обьекте {2}, делая {3}, записал себе {4} часов {5} минут {6} секунд".format(
                                 name_from_base, surname_from_base, last_project_name_from_base,
                                 last_job_from_base, hours, minutes, seconds))

        else:
            minutes = 0
            hours = 0
            prev_time = globaltime[message.chat.id]
            now = time.time()
            seconds = int(now - prev_time)
            if seconds >= 60:
                minutes = seconds // 60
                seconds = seconds % 60
            if minutes >= 60:
                hours = minutes // 60
                minutes = minutes % 60

            Workers.update_one({"Telegram": message.chat.id},
                               {"$set": {"Last lat": message.location.latitude,
                                         "Last lng": message.location.longitude}})

            time_list = user_dict['Total time'].split(":")
            hours_from_base = int(time_list[0])

            minutes_from_base = int(time_list[1])

            seconds_from_base = int(time_list[2])

            full_hours = hours + hours_from_base
            full_minutes = minutes + minutes_from_base
            full_secounds = seconds + seconds_from_base
            if full_secounds >= 60:
                full_minutes = full_minutes + (full_secounds // 60)
                full_secounds = full_secounds % 60
            if full_minutes >= 60:
                full_hours = full_hours + (full_minutes // 60)
                full_minutes = full_minutes % 60
            time_totally = str(full_hours) + ":" + str(full_minutes) + ":" + str(full_secounds)
            Workers.update_one({"Telegram": message.chat.id},
                               {"$set": {"Total time": time_totally}})
            fresh_time = str(hours) + ":" + str(minutes) + ":" + str(seconds)
            History.insert_one(
                {"Telegram": message.chat.id, "Name": name_from_base, "Surname": surname_from_base,
                 "Time written": fresh_time, "Time": time.time(),
                 "Project": last_project_name_from_base, "Work": last_job_from_base, "Correct": False})
            bot.send_message(message.chat.id,
                             "За сегодня вы получили {0} часов {1} минут {2} секунд, делая {3} на обьекте {4}, но таймер был остановлен НЕКОРРЕКТНО".format(
                                 hours, minutes, seconds, message.text, last_project_name_from_base))
            bot.send_message(403316002,
                             "Пользователь {0} {1} остановил таймер НЕКОРРЕКТНО, начав работу на обьекте {2}, делая {3}. Записанное время:{4} часов {5} минут {6} секунд. Последние координаты: Lat: {7} Lng: {8} ".format(
                                 name_from_base, surname_from_base, last_project_name_from_base,
                                 last_job_from_base, hours, minutes, seconds, message.location.latitude,
                                 message.location.longitude))
            bot.send_message(message.chat.id,
                             "Ваше общее время: {0} часов , {1} минут , {2} секунд".format(full_hours, full_minutes,
                                                                                           full_secounds))

    else:
        bot.send_message(message.chat.id, "Я ожидаю вашу геолокацию")
        bot.register_next_step_handler(message, location_stopper)


@bot.message_handler(commands=['time', 'stop', 'begin'])
def free_time_function(message):
    if message.text == "/time":
        time_value = Workers.find_one({"Telegram": message.chat.id})["Total time"]
        bot.send_message(message.chat.id,
                         f"Ваше время: {time_value}")

    elif message.text == "/begin":
        project_choice(message)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Нечего останавливать, таймер не был запущен")

    else:
        bot.send_message(message.chat.id, "Ваше сообщение не корректно")


bot.polling(none_stop=True, timeout=123)
