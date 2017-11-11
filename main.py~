from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

currencyinfo = False
convert = False
def start(bot, update):
    keyboard = [[InlineKeyboardButton("/market", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def help(bot, update):
    update.message.reply_text('Need help? Fuck yourself')

def currencyInfo(bot, update):
    currencyinfo = True
    chooseCurrency(bot, update)

def Convert(bot, update):
    convert = True
    chooseCurrency(bot, update)


def chooseCurrency(bot, update):
    kb = [[KeyboardButton(text="BTC"), KeyboardButton(text="ETH"),KeyboardButton(text="BCH")],
          [KeyboardButton(text="XRP"), KeyboardButton(text="LTC"), KeyboardButton(text="DASH")]]
    bot.sendMessage(update.message.chat.id, "What currency do you want info on?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=kb
        )
    )



def answerer(bot, update):
    if currencyinfo:
        pass

    if convert:
        pass

    update.message.reply_text("in reader")


def button(bot, update):
    query = update.callback_query
    if query.data == "1":
        return marketInfo(bot, update)

def main():

    with open('TelegramToken.txt', 'r') as tokentxt:
        # Obtenir d'un arxiu txt el token únic del bot en qüestió
        token = tokentxt.readline().strip()

    botUpdater = Updater(token)
    bot = botUpdater.dispatcher

    # Events
    #   Commandos: comencen amb /
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("market", marketInfo))
    bot.add_handler(CommandHandler("help", help))
    #   Missatges: Filtrar els de text
    bot.add_handler(MessageHandler(Filters.text, answerer))
    #   Botons
    bot.add_handler(CallbackQueryHandler(button))

    botUpdater.start_polling()
    botUpdater.idle()

if __name__ == "__main__":
    main()
