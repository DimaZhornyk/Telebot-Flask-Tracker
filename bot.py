from sqlalchemy import select
import telebot
from connection import Locations, Global, engine
from telebot import types
import time

bot = telebot.TeleBot('973520242:AAH8WeGRmUNqKzYDdM1PCURHoojkNYWATwU')
globaltime = {}


def count_locations():
    conn = engine.connect()
    locations = conn.execute(select([Locations.c.id])).fetchall()
    return len(locations)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет, я ваш бот. Я умею считать ваше рабочее время и показывать накопленные часы. "
                     "Делаю я это только если вы находтесь на рабочем месте. Для начала работы, нажмите /go")


@bot.message_handler(commands=['go'])
def name_listener(message):
    try:
        conn = engine.connect()
        outname = conn.execute(select([Global.c.name]).where(Global.c.id == message.chat.id)).fetchall()
    except IndexError:
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
    conn = engine.connect()
    conn.execute(
        Global.insert().values(id=message.chat.id, name=message.text, surname='', total_hours=0, total_minutes=0,
                               total_seconds=0, last_project='', last_job='', lastLat=0, lastLng=0, project_chosen=''))
    bot.send_message(message.chat.id, 'Введите свою фамилию')
    bot.register_next_step_handler(message, surname_handler)


def surname_handler(message):
    conn = engine.connect()
    conn.execute(Global.update().values(surname=message.text).where(Global.c.id == message.chat.id))
    bot.send_message(message.chat.id, '''Регистрация прошла успешно, тепер вы можете использовать бота. Его команды:
        /begin для начала отсчета
        /stop для окончания отсчета
        /time для отображения накопленного времени''')


def project_choice(message):
    bot.send_message(message.chat.id, "Выберите обьект на котором вы работаете: ")
    conn = engine.connect()
    for i in range(0, count_locations()):
        locname_from_base = conn.execute(select([Locations.c.name])).fetchall()[i][0]
        bot.send_message(message.chat.id, "/{0} чтобы выбрать {1}".format(i + 1, locname_from_base))
    bot.register_next_step_handler(message, geo)


def geo(message):
    if message.text[1:].isdigit():
        try:
            conn = engine.connect()
            proj_ident = conn.execute(select([Locations.c.id])).fetchall()[int(message.text[1:])-1][0]
            conn.execute(Global.update().values(project_chosen=proj_ident).where(Global.c.id == message.chat.id))
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
            keyboard.add(button_geo)
            bot.send_message(message.chat.id,
                             "Нажмите на кнопку и передайте мне свое местоположение или нажмите /back для возврата в главное меню",
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, location_new)
        except:
            bot.send_message(message.chat.id, "Некорректный ввод")
            bot.register_next_step_handler(message, geo)

    else:
        bot.send_message(message.chat.id, "Некорректный ввод")
        bot.register_next_step_handler(message, geo)


def location_new(message):
    conn = engine.connect()
    proj_ident = conn.execute(select([Global.c.project_chosen]).where(Global.c.id == message.chat.id)).fetchall()[0][0]
    if message.location:
        latitude_from_base = conn.execute(select([Locations.c.lat]).where(Locations.c.id == proj_ident)).fetchall()[0][
            0]
        longitude_from_base = conn.execute(select([Locations.c.lng]).where(Locations.c.id == proj_ident)).fetchall()[0][
            0]

        if latitude_from_base - 0.004 < message.location.latitude < latitude_from_base + 0.004 and \
                longitude_from_base - 0.004 < message.location.longitude < longitude_from_base + 0.04:
            now = time.time()
            globaltime[message.chat.id] = now
            bot.send_message(message.chat.id,
                             "Ваша локация соответствует необходимой, счетчик запущен. Для его остановки нажмите /stop  ")
            conn.execute(Global.update().values(last_project=proj_ident).where(Global.c.id == message.chat.id))
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
    conn = engine.connect()
    conn.execute(Global.update().values(last_job=message.text).where(Global.c.id == message.chat.id))
    bot.send_message(message.chat.id, "Теперь повторно отправьте свою геолокацию чтобы остановить таймер")
    bot.register_next_step_handler(message, location_stopper)


def location_stopper(message):
    conn = engine.connect()
    if message.location:
        lastproject_from_base = conn.execute(
            select([Global.c.last_project]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

        latitude_from_base = conn.execute(
            select([Locations.c.lat]).where(Locations.c.id == lastproject_from_base)).fetchall()[0][0]

        longitude_from_base = conn.execute(
            select([Locations.c.lng]).where(Locations.c.id == lastproject_from_base)).fetchall()[0][0]

        name_from_base = conn.execute(
            select([Global.c.name]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

        surname_from_base = conn.execute(
            select([Global.c.surname]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

        last_project_name_from_base = conn.execute(
            select([Locations.c.name]).where(Locations.c.id == lastproject_from_base)).fetchall()[0][0]

        last_job_from_base = conn.execute(
            select([Global.c.last_job]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

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

            conn.execute(
                Global.update().values(lastLat=message.location.latitude, lastLng=message.location.longitude).where(
                    Global.c.id == message.chat.id))

            hours_from_base = conn.execute(
                select([Global.c.total_hours]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

            minutes_from_base = conn.execute(
                select([Global.c.total_minutes]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

            seconds_from_base = conn.execute(
                select([Global.c.total_seconds]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

            full_hours = hours + hours_from_base
            full_minutes = minutes + minutes_from_base
            full_secounds = seconds + seconds_from_base
            if full_secounds >= 60:
                full_minutes = full_minutes + (full_secounds // 60)
                full_secounds = full_secounds % 60
            if full_minutes >= 60:
                full_hours = full_hours + (full_minutes // 60)
                full_minutes = full_minutes % 60
            conn.execute(
                Global.update().values(total_hours=full_hours, total_minutes=full_minutes, total_seconds=full_secounds).where(
                    Global.c.id == message.chat.id))
            bot.send_message(message.chat.id,
                             "За сегодня вы получили {0} часов {1} минут {2} секунд, делая {3} на обьекте {4} - {5}".format(
                                 hours, minutes, seconds, last_job_from_base, lastproject_from_base,
                                 last_project_name_from_base))
            bot.send_message(message.chat.id,
                             "Ваше общее время: {0} часов , {1} минут , {2} секунд".format(full_hours, full_minutes,
                                                                                           full_secounds))
            bot.send_message(403316002,
                             "Пользователь {0} {1} остановил таймер корректно, начав работу на обьекте {2} - {3}, делая {4}, записал себе {5} часов {6} минут {7} секунд".format(
                                 name_from_base, surname_from_base, lastproject_from_base, last_project_name_from_base,
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

            conn.execute(
                Global.update().values(lastLat=message.location.latitude, lastLng=message.location.longitude).where(
                    Global.c.id == message.chat.id))

            hours_from_base = conn.execute(
                select([Global.c.total_hours]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

            minutes_from_base = conn.execute(
                select([Global.c.total_minutes]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

            seconds_from_base = conn.execute(
                select([Global.c.total_seconds]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

            full_hours = hours + hours_from_base
            full_minutes = minutes + minutes_from_base
            full_secounds = seconds + seconds_from_base
            if full_secounds >= 60:
                full_minutes = full_minutes + (full_secounds // 60)
                full_secounds = full_secounds % 60
            if full_minutes >= 60:
                full_hours = full_hours + (full_minutes // 60)
                full_minutes = full_minutes % 60
            conn.execute(
                Global.update(total_hours=full_hours, total_minutes=full_minutes, total_seconds=full_secounds).where(
                    Global.c.id == message.chat.id))
            bot.send_message(message.chat.id,
                             "За сегодня вы получили {0} часов {1} минут {2} секунд, делая {3} на обьекте {4} - {5}, но таймер был остановлен НЕКОРРЕКТНО".format(
                                 hours, minutes, seconds, message.text, lastproject_from_base,
                                 last_project_name_from_base))
            bot.send_message(403316002,
                             "Пользователь {0} {1} остановил таймер НЕКОРРЕКТНО, начав работу на обьекте {2} - {3}, делая {4}. Записанное время:{5} часов {6} минут {7} секунд. Последние координаты: Lat: {8} Lng: {9} ".format(
                                 name_from_base, surname_from_base, lastproject_from_base, last_project_name_from_base,
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
    conn = engine.connect()
    if message.text == "/time":
        hours_from_base = conn.execute(
            select([Global.c.total_hours]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

        minutes_from_base = conn.execute(
            select([Global.c.total_minutes]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

        seconds_from_base = conn.execute(
            select([Global.c.total_seconds]).where(Global.c.id == message.chat.id)).fetchall()[0][0]

        bot.send_message(message.chat.id,
                         "Ваше время: {0} часов , {1} минут , {2} секунд".format(hours_from_base, minutes_from_base,
                                                                                 seconds_from_base))

    elif message.text == "/begin":
        bot.send_message(message.chat.id, "Выберите обьект на котором вы работаете: ")
        for i in range(0, count_locations()):
            locname_from_base = conn.execute(select([Locations.c.name])).fetchall()[i][0]
            bot.send_message(message.chat.id, "/{0} чтобы выбрать {1}".format(i + 1, locname_from_base))
        bot.register_next_step_handler(message, geo)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Нечего останавливать, таймер не был запущен")

    else:
        bot.send_message(message.chat.id, "Ваше сообщение не корректно")


bot.polling(none_stop=True, interval=0)
