import os
import requests

from telebot import TeleBot, types
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('TOKEN')
my_chat_id = os.getenv('MY_CHAT_ID')
url = os.getenv('URL')
second_url = os.getenv('SECOND_URL')
weather_api_key = os.getenv('WEATHER_API_KEY')
weather_url = (f'https://api.weatherapi.com/v1/current.json'
               f'?key={weather_api_key}&q=Shanghai')


bot = TeleBot(token=token)


@bot.message_handler(func=lambda message: message.from_user.id == my_chat_id)
def answer_to_boss(message):
    bot.send_message(chat_id=my_chat_id, text='hey boss')


def get_new_img():
    try:
        response = requests.get(url).json()
    except Exception as error:
        print(error)
        response = requests.get(second_url).json()
    random_cat = response[0].get('url')
    return random_cat


@bot.message_handler(commands=['newcat'])
def send_new_cat(message):
    chat_id = message.chat.id
    bot.send_photo(chat_id=chat_id, photo=get_new_img())


@bot.message_handler(commands=['weather'])
def weather(message):
    chat_id = message.chat.id
    response = requests.get(weather_url).json()
    weather_info = (f"Температура в Шанхае сейчас: "
                    f"{response['current']['temp_c']}°C "
                    f"Ощущается как {response['current']['feelslike_c']}")
    bot.send_message(chat_id=chat_id, text=weather_info)


@bot.message_handler(commands=['help', 'start'])
def wake_up(message):
    chat = message.chat
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('/newcat'),
                 types.KeyboardButton('/weather'),
                 types.KeyboardButton('/about_me'),
                 types.KeyboardButton('/help'),
                 row_width=2)
    bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что вы включили меня, {chat.first_name}! '
        f'Если вы хотите узнать погоду в Шанхае, нажмите /weather,'
        f' если узнать о своем профиле в Телеграм - нажмите'
        f' /about_me, если хотите посмотреть казахского котика - /newcat.'
        f' Кстати, вот и фото одного из казахских котиков ниже!',
        reply_markup=keyboard
    )
    bot.send_photo(chat_id=chat.id,
                   photo=get_new_img())


@bot.message_handler(commands=['about_me'])
def about_me(message):
    chat = message.chat
    chat_user = message.from_user
    bot.send_message(chat_id=chat.id,
                     text=f'Ваше имя: {chat.first_name} {chat.last_name}.'
                     f' Ваш id - {chat.id}. Ваш username - {chat.username}.'
                     f' Ваш язык - {chat_user.language_code}.')


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Выберите команду из списка команд')


@bot.message_handler(content_types=['sticker', 'dice', 'photo', 'animation'])
def response_to_sticker(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text='Давайте не картинки тут слать а выбирать команду')


def main():
    bot.polling(interval=20)


if __name__ == '__main__':
    main()
