from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from coinmarketcap import Market

currencyinfo = False
conversion = False
conversionEur = -1
waitingamount = False
waitingnumcurrencies = False
waitingtarget = False
rate = [None, 0]


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Donate", callback_data='1', url="paypal.me/tetacos")],
                [InlineKeyboardButton("Code", callback_data='2', url="https://github.com/andreuinyu/Coinbot")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to Coinbot. Send /help for information on how to use', reply_markup=reply_markup)


def help(bot, update):
    msg = "This bot helps you get useful info on cryptocurrencies. \n\n" \
          "*Market info* \n /market - It will show you the _n_ most relevant cryptocurrencies and its status \n" \
          "*Graph* \n /graph - Last 6 months of the bitcon price in USD\n" \
          "*Currency*\n /currency - Given a code of a cryptocurrency, displays its name, the existing supply and the " \
          "daily and weekly change in value\n" \
          "*Convert* \n /convert - get the conversion from cryptocurrency of your choice to Euros, US Dollars, Swiss Francs or Pounds"
    bot.sendMessage(update.message.chat.id, msg, parse_mode="Markdown")


def currencyInfo(bot, update):
    global currencyinfo
    currencyinfo = True
    chooseCurrency(bot, update)


def Convert(bot, update):
    global waitingtarget
    global waitingamount
    waitingtarget = True
    waitingamount = True
    chooseConversion(bot, update)


def chooseConversion(bot, update):
    kb = [[KeyboardButton(text="USD"), KeyboardButton(text="EUR")],
          [KeyboardButton(text="CHF"), KeyboardButton(text="GBP")]]
    bot.sendMessage(
        update.message.chat.id,
        "Choose real currency target:",
        reply_markup=ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
    )


def chooseCurrency(bot, update):
    coinmarketcap = Market()
    array = coinmarketcap.ticker(limit=6)
    kb = []
    i = 0
    for fila in range(2):
        kb.append([])
        for col in range(3):
            kb[fila].append(KeyboardButton(text=array[i]["symbol"]))
            i += 1
    bot.sendMessage(
        update.message.chat.id,
        "Choose or type the desired cryptocurrency symbol:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=kb,
            one_time_keyboard=True
        )
    )


def marketInfo(bot, update):
    global waitingnumcurrencies
    waitingnumcurrencies = True
    update.message.reply_text("Get me the top")


def answerer(bot, update):
    text = update.message.text

    global currencyinfo
    global conversion
    global conversionEur
    global rate
    global waitingamount
    global waitingnumcurrencies
    global waitingtarget

    if currencyinfo:
        found = False
        coinmarketcap = Market()
        array = coinmarketcap.ticker(limit=100)
        for moneda in array:
            if moneda["symbol"] == text:
                found = True
                info = "Name: " + moneda["name"] + ' (' + moneda['symbol'] + ')'+"\nRanked: "
                info += moneda['rank']+ "\nSupply: " + moneda["available_supply"] + " of "
                if moneda["max_supply"] is None:
                    info += "unknown \n"
                else:
                    info += moneda["max_supply"] + text +  " ("+ str(int(float(moneda["available_supply"])/float(moneda["max_supply"]) * 100))+"%)"+"\n"
                info += "Value change 24h: " + moneda["percent_change_24h"] + "%"
                info += "\nValue change 7 day: " + moneda["percent_change_7d"] + "%"
                update.message.reply_text(info)
                break
        if not found:
            update.message.reply_text("Cryptocurrency not found, choose another currency")
        else:
            currencyinfo = False

    elif waitingtarget and conversionEur == -1:
        waitingtarget = False
        if text == 'USD':
            conversionEur = 0
        elif text == "EUR":
            conversionEur = 1
        elif text == "CHF":
            conversionEur = 2
        elif text == "GBP":
            conversionEur = 3
        conversion = True
        chooseCurrency(bot, update)

    elif conversion and conversionEur != -1:
        conversion = False
        coinmarketcap = Market()
        if conversionEur == 1:
            array = coinmarketcap.ticker(limit=100, convert='EUR')
        elif conversionEur == 2:
            array = coinmarketcap.ticker(limit=100, convert='CHF')
        elif conversionEur == 3:
            array = coinmarketcap.ticker(limit=100, convert='GBP')
        else:
            array = coinmarketcap.ticker(limit=100, convert="USD")
        for moneda in array:
            if text == moneda["symbol"]:
                rate[0] = text
                if conversionEur == 1:
                    rate[1] = float(moneda["price_eur"])
                elif conversionEur == 2:
                    rate[1] = float(moneda["price_chf"])
                elif conversionEur == 3:
                    rate[1] = float(moneda["price_gbp"])
                else:
                    rate[1] = float(moneda["price_usd"])
                waitingamount = True
                break
        update.message.reply_text("Enter amount of " + rate[0])

    elif waitingamount:
        waitingamount = False
        preu = "{:.2f}".format(float(text)*rate[1])
        if conversionEur == 0:
            update.message.reply_text(text + " " + rate[0] + " = $" + preu)
        elif conversionEur == 1:
            update.message.reply_text(text + " " + rate[0] + " = " + preu + "€")
        elif conversionEur == 2:
            update.message.reply_text(text + " " + rate[0] + " = " + preu + "Fr.")
        elif conversionEur == 3:
            update.message.reply_text(text + " " + rate[0] + " = £" + preu)
        conversionEur = -1

    elif waitingnumcurrencies:
        if text.isdigit():
            waitingnumcurrencies = False
            out = "Summary of the top {} cryptocurrencies by market cap: \n".format(text)
            coinmarketcap = Market()
            array = coinmarketcap.ticker(limit=int(text))
            for moneda in array:
                out += '\n' + moneda['name'] + ' (' + moneda['symbol'] + ')' + ' = $' + moneda['price_usd']
            update.message.reply_text(out)
        else:
            update.message.reply_text("Only integers")


def graph(bot, update):
    img = "https://bitcoincharts.com/charts/chart.png?width=940&m=bitmarketEUR&SubmitButton=Draw&r=180&i=&c=0&s=&e=&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&"
    bot.sendPhoto(update.message.chat.id, img)


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
    bot.add_handler(CommandHandler("currency", currencyInfo))
    bot.add_handler(CommandHandler("convert", Convert))
    #   Missatges: Filtrar els de text
    bot.add_handler(MessageHandler(Filters.text, answerer))

    botUpdater.start_polling()
    botUpdater.idle()


if __name__ == "__main__":
    main()
