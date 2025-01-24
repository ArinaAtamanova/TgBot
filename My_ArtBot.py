import telebot
import schedule
import time
import random
from threading import Thread

TOKEN = "7771824400:AAEbgP15U9yFOeHtHSzeqawXrXSwwShgs4I"
CHAT_ID = "@arinalien_bot"
bot = telebot.TeleBot(TOKEN)

# Список заданий
TASKS = {
    1: "Изучить 10-15 иллюстраторов Bang Bang и записать заметки.",
    2: "Попробовать 2-3 стиля в мини-эскизах.",
    3: "Разработать идеи для 3 проектов.",
    4: "Начать работу над первым проектом: композиция + эскизы.",
    5: "Доработка деталей и цвет первого проекта.",
    6: "Начать работу над вторым проектом: композиция + эскизы.",
    7: "Финализация второго проекта: детали и цвет."
}

# Список наград
REWARDS = [
    "🎬 Интересный фильм о художниках: https://www.imdb.com/title/tt0119822/",
    "🎨 Факт: Ван Гог продал всего одну картину за свою жизнь!",
    "📖 Полезная статья об иллюстрации: https://medium.com/design-articles",
    "🖌 Интересный арт-челлендж: нарисую иллюстрацию маслянной пателью на формате а3",
    "🎭 Биография великого художника: https://www.biography.com/artist",
    "📺 Видео с разбором стилей иллюстраторов: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
]

user_progress = {}  # Хранит выполненные задания

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я твой бот-наставник. Буду отправлять тебе задания каждый день.")
    send_task()

# Функция отправки задания
def send_task():
    day = len(user_progress) + 1
    if day in TASKS:
        bot.send_message(CHAT_ID, f"🎯 Задание дня {day}: {TASKS[day]}")
    else:
        bot.send_message(CHAT_ID, "✅ Все задания выполнены! Время отправить заявку в Bang Bang.")

# Функция для отметки выполнения и выдачи награды
@bot.message_handler(commands=['done'])
def mark_done(message):
    day = len(user_progress) + 1
    user_progress[day] = True
    bot.send_message(message.chat.id, f"✅ Задание {day} выполнено!")
    reward = random.choice(REWARDS)
    bot.send_message(message.chat.id, f"🏆 Награда за выполнение: {reward}")
    send_task()

# Запуск задания каждый день
def daily_task():
    send_task()

schedule.every().day.at("10:00").do(daily_task)  # Отправлять задание каждый день в 10 утра

# Штраф за невыполнение задания
schedule.every().day.at("22:00").do(lambda: bot.send_message(CHAT_ID, "❌ Ты не выполнил задание! Штраф: отложенный бонус!"))

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Запуск бота и потока для проверки штрафов
Thread(target=schedule_checker).start()
bot.polling()
