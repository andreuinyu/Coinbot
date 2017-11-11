from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import coinbase as cb

processingsend = False
waitingemail = False
waitingamount = False


def start(bot, update):
    global token
    responseurl = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text=".format(token, update.message.chat.id)
    coinbase_oauth = cb.CoinbaseOAuth("bf03ac56dd01694ba744831afdbcc94abbc9f36d804c59b5904f4549be2e4047",
                                      "38bc50fcef5a87f9703fcc5939c75edbd00b70244fe1d34ddd40a5b05b2f40db",
                                      responseurl)
    authurl = coinbase_oauth.create_authorize_url()
    authurl = authurl[0:-6] + "&scope=balance+addresses+user+transactions"
    msg = "[Allow access:]({})".format(authurl)
    update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


def help(bot, update):
    update.message.reply_text('Need help? Fuck yourself')


def send(bot, update):
    global processingsend
    global waitingemail
    global waitingamount
    processingsend = True
    waitingemail = True
    waitingamount = True
    update.message.reply_text('Send me the email of the receiver')


def answerer(bot, update):

    global processingsend
    global waitingemail
    global waitingamount
    text = update.message.text
    #update.message.reply_text("in reader")
    #print(processingsend)

    if processingsend  and waitingemail  :
        email = text
        waitingemail = False
        update.message.reply_text("got email, enter amount")
    elif processingsend == True and waitingamount == True:
        amount = text
        update.message.reply_text("got amount")
        waitingamount = False
        processingsend = False

        """
        response = cb.send_money('user@example.com', '2')
        print(response['success'])
        # True
        print(response['transaction']['status'])
        # 'pending'
        print(response['transaction']['id'])
        # '518d8567ed3ddcd4fd000034'
        """

def main():

    global token
    processingsend = False
    waitingemail = False
    waitingamount = False

    with open('TelegramToken.txt', 'r') as tokentxt:
        # Obtenir d'un arxiu txt el token únic del bot en qüestió
        token = tokentxt.readline().strip()
    botUpdater = Updater(token)
    bot = botUpdater.dispatcher

    # Events
    #   Commandos: comencen amb /
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("send", send))
    bot.add_handler(CommandHandler("help", help))
    #   Missatges: Filtrar els de text
    bot.add_handler(MessageHandler(Filters.text, answerer))

    botUpdater.start_polling()
    botUpdater.idle()


if __name__ == '__main__':
    main()
