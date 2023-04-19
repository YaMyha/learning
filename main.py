import telebot
from telebot.types import Message
import json
import requests
from datetime import datetime
from envparse import Env
from telegram_client import TelegramClient
from sql_and_user import SQLiteClient, UserActioner

env = Env()
TOKEN = env.str("TOKEN")
ADMIN_CHAT_ID = env.int("ADMIN_CHAT_ID")

class MyBot(telebot.TeleBot):
    def __init__(self, telegram_client: TelegramClient, user_actioner: UserActioner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telegram_client = telegram_client
        self.user_actioner = user_actioner

    def setup_resources(self):
        self.user_actioner.setup()

telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")
user_actioner = UserActioner(SQLiteClient("users.db"))
bot = MyBot(token=TOKEN, telegram_client=telegram_client, user_actioner=user_actioner)
bot.setup_resources()

@bot.message_handler(commands=["start"])
def start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    create_new_user = False

    user = bot.user_actioner.get_user(user_id)

    if not user:
        bot.user_actioner.create_user(user_id=str(user_id), username=username, chat_id=chat_id)
        create_new_user = True

    bot.reply_to(message=message, text=f"Вы {'' if create_new_user else 'уже'} зарегистрированы: {username}. "
                                                  f"Ваш user_id: {user_id}")
    # with open("users.json", "r") as f_o:
    #     data_from_json = json.load(f_o)
    #
    # if str(user_id) not in data_from_json:
    #     data_from_json[user_id] = {"username": username}
    # with open("users.json", "w") as f_o:
    #     json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    # # print(data_from_json)

def handle_standup_speech(message: Message):
    bot.reply_to(message, text='Пон')


@bot.message_handler(commands=["say_standup_speech"])
def say_standup_speech(message: Message):
    print("К Т О - Т О  В Ы З В А Л  К О М А Н Д У ! ! !")
    bot.reply_to(message=message, text='Ну рассказывай!')
    img = open("C:/Users/Professional/Desktop/Python/tb/image.jpg", 'rb')
    bot.send_photo(message.chat.id, img)
    bot.register_next_step_handler(message, handle_standup_speech)

def create_error_message(err: Exception) -> str:
    return f"{datetime.now()}:::{err.__class__}:::{err}"

while True:
    try:
        bot.polling()
    except Exception as err:
        bot.telegram_client.post(method="sendMessage", params={"text": create_error_message(err),
                                                               "chat_id":ADMIN_CHAT_ID})