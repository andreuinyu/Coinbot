from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import coinbase as cb


def start(bot, update):
    update.message.reply_text("sanx marika")


def help(bot, update):
    update.message.reply_text('Need help? Fuck yourself')


def answerer(bot, update):
    text = update.message.text
    update.message.reply_text(reverse(text))


def reverse(s):
    #Tonterida de funció
    ans = ''
    for c in s:
        ans = c + ans
    return ans


def main():
    coinbase_oauth = cb.CoinbaseOAuth("bf03ac56dd01694ba744831afdbcc94abbc9f36d804c59b5904f4549be2e4047",
                                      "38bc50fcef5a87f9703fcc5939c75edbd00b70244fe1d34ddd40a5b05b2f40db",
                                      "https://www.t.me/CoBase_bot")
    authurl = coinbase_oauth.create_authorize_url()
    authurl= authurl[0:-6] + "&scope=balance+addresses+user+transactions"

    print(authurl)

    with open('TelegramToken.txt', 'r') as tokentxt:
        # Obtenir d'un arxiu txt el token únic del bot en qüestió
        token = tokentxt.readline().strip()
    botUpdater = Updater(token)
    bot = botUpdater.dispatcher



    # Events
    #   Commandos: comencen amb /
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("help", help))
    #   Missatges: Filtrar els de text
    bot.add_handler(MessageHandler(Filters.text, answerer))

    botUpdater.start_polling()
    botUpdater.idle()

if __name__ == '__main__':
    main()
