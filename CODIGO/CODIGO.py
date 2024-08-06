import telebot
from TOKEN import TOKEN
from telebot import types
import re
import json

bot = telebot.TeleBot(TOKEN)

with open('CONFIG.json', 'r') as config_file:
    config = json.load(config_file)
universal_punishment = config['punishment']

with open('PALAVRAS.txt', 'r') as palavras_file:
    palavras_proibidas = [linha.strip().lower() for linha in palavras_file.readlines()]

@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "Olá! Sou um bot moderador de grupos.")
    else:
        if message.from_user.id in [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]:
            bot.send_message(message.chat.id, "VOCÊ É ADM")
        else:
            bot.send_message(message.chat.id, "VOCÊ NÃO É ADM")

def apply_punishment(message, punishment):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    if message.from_user.id != bot.get_me().id:  
        if punishment == "ban":
            bot.kick_chat_member(message.chat.id, message.from_user.id)
        elif punishment == "mute":
            bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions())
        elif punishment == "kick":
            bot.kick_chat_member(message.chat.id, message.from_user.id)
        elif punishment == "off":
            pass 

@bot.message_handler(func=lambda message: True)
def anti_palavrao(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.lower()

    if not message.from_user.is_bot:
        member = bot.get_chat_member(chat_id, user_id)
        if not member.status in ["creator", "administrator"]:
            for palavra in palavras_proibidas:
                if palavra in text:
                    bot.delete_message(chat_id, message.message_id)
                    apply_punishment(message, universal_punishment)
                    bot.send_message(chat_id, f"Usuário {message.from_user.first_name} foi punido por usar linguagem inadequada!")
                    break

if __name__ == '__main__':
    print("Bot Iniciado!")
    bot.polling()
