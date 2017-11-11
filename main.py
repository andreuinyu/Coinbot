from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from coinmarketcap import Market

currencyinfo = False;
conversion = False;

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
    coinmarketcap = Market()
    array = coinmarketcap.ticker(limit=6)
    kb = []
    i = 0
    for fila in range(2):
        kb.append([])
        for col in range(3):
            kb[fila].append(KeyboardButton(text=array[i]["symbol"]))
            i+=1
    bot.sendMessage(update.message.chat.id, "What currency do you want info on?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=kb
        )
    )

def marketInfo(bot, update):
    out = "Summary of the top cryptocurrencies by market cap: \n"
    coinmarketcap = Market()
    array = coinmarketcap.ticker(limit=10)
    for moneda in array:
        out +='\n' + moneda['name'] +' ('+ moneda['symbol'] +')' +' = $' + moneda['price_usd']
    update.message.reply_text(out)

def answerer(bot, update):
    if currencyinfo:
        pass

    if convert:
        pass

    update.message.reply_text("in reader")


def graph(bot,update):
    #bitcoin usd
    img= "https://bitcoincharts.com/charts/chart.png?width=940&m=bitstampUSD&SubmitButton=Draw&r=180&i=&c=0&s=&e=&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&"
    #update.message.reply_text(img)
    bot.sendPhoto(update.message.chat.id, img)

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
    bot.add_handler(CommandHandler("graph", graph))
    bot.add_handler(CommandHandler("currency", chooseCurrency))
    #   Missatges: Filtrar els de text
    bot.add_handler(MessageHandler(Filters.text, answerer))
    #   Botons
    bot.add_handler(CallbackQueryHandler(button))

    botUpdater.start_polling()
    botUpdater.idle()

if __name__ == "__main__":
    main()
