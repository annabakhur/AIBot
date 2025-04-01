from config import TOKEN
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import random

bot = telebot.TeleBot(TOKEN)

url = "https://rb.ru/list/the-most-interesting-neural-networks/"
page = BeautifulSoup(requests.get(url).content, 'html.parser')

tags = page.find('li', dir="ltr")
names_before = tags.find_all('a', class_="smooth_scroll")
names_before.pop(0)
names_before.pop(-1)
names = []
for name in names_before:
    names.append(name.find('strong').text)

links = [
    'https://ya.ru/ai/gpt',
    'https://giga.chat/',
    'https://chatgpt.com/',
    'https://copilot.microsoft.com/',
    'https://gemini.google.com/'
]

info = [
    "Большая языковая модель от Яндекса...",
    "Языковая модель от Сбера...",
    "Одна из самых известных моделей в мире...",
    "Инструмент для помощи разработчикам...",
    "Мультимодальная модель от Google..."
]

ai_data = {}
for i in range(len(names)):
    ai_data[names[i]] = {'url': links[i], 'info': info[i]}

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Используйте команду /networks для вывода списка нейросетей")

@bot.message_handler(commands=["networks"])
def show_networks(message):
    markup = types.InlineKeyboardMarkup()
    for name in names:
        markup.add(types.InlineKeyboardButton(name, callback_data=name))
    markup.add(types.InlineKeyboardButton("Случайная нейросеть", callback_data="random_ai"))
    bot.send_message(message.chat.id, "Выберите нейросеть:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data)
def callback_query(call):
    ai_name = random.choice(names) if call.data == "random_ai" else call.data
    data = ai_data.get(ai_name, {})
    response = f"Вы выбрали: {ai_name}.\nСсылка: {data.get('url', 'Нет данных')}\nОписание: {data.get('info', 'Нет данных')}"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, response)

bot.polling()
