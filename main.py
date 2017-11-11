from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(bot, update):
    update.message.reply_text('')


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
    with open('TelegramToken.txt', 'r') as tokentxt:
        #Obtenir d'un arxiu txt el token únic del bot en qüestió
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