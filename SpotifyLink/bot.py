import os
import spotify_api
import telebot

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def no_patience(message):
    bot.send_message(message.chat.id, "yo")


@bot.message_handler(commands=['search'])  # fix
def search(message):
    msg = message.text.split()
    if (len(msg) > 2) and (msg[1] == "track"):
        search_arg = " ".join(msg[2:])
        track_link = spotify_api.get_track_link(search_arg)
        bot.send_message(message.chat.id, track_link)
    if (len(msg) > 2) and (msg[1] == "album"):
        search_arg = " ".join(msg[2:])
        if "hipster" in search_arg:
            album_link = spotify_api.get_album_link(search_arg, True)
        else:
            album_link = spotify_api.get_album_link(search_arg, False)
        bot.send_message(message.chat.id, album_link)
    else:
        bot.send_message(message.chat.id, "here's how this command works: \n\n"
                                          "/search [type] [search] \n\n"
                                          "[type]: track\\album\\artist\\etc. \n"
                                          "[search]: ur search arg for spotify catalog ")


@bot.message_handler(commands=["dice"])
def ask_the_Gods(message):
    bot.send_dice(message.chat.id)


@bot.message_handler(func=lambda x: True)
def invalid(message):
    bot.send_message(message.chat.id, "invalid request")


bot.infinity_polling()