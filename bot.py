import atexit
import sys

import this
from threading import Thread
import discum as discum

import get_asset_image
import variables
from Commands import init

print("Bot started!")





# data
BotUsername = "BABUIN-FM"
ChannelId = "1062353490535514222"#"1040630178566656161"
token = 'MTA3MTUxMTIzMjU1ODk0MDMwMA.Gasrif.4E-W_bX1qvHZmi7kB3zXM8BtQnxBst4uQm5EhI'


bot = discum.Client(token=token, log=False)
# settings
HelpSay = "Я бабуин версии - ROBLOX UGC LIMITEDS SNIPER. Сейчас я не начал работу, чтобы это произошло скажите: `Бабуин начни работу`. Что я могу - `Бабуин добавь лимитку: id`, `Бабуин убери лимитку: id`, `Бабуин покажи лимитки`, `Бабуин +пауза`, `Бабуин -пауза`, `Бабуин отключись`, `Бабуин что за предмет`. Последнее отключает UGC - Sniper."
IListenSay = "Хорошо, я вас слушаю"
WaitSay = "Ожидайте"

# Memory
this.Commands = []

this.ListeningUsers = []
this.PlayersCommands = [[]]


variables.LIMITS = []
variables.PAUSE = True


this.ListeningUsers.append(["123", "321"])
print(this.ListeningUsers)

init() # Подгрузка команд

# CommandFunctions
def HelpCommand(content, username, messageID, args, args2):
    bot.sendMessage(ChannelId, HelpSay)

def CheckListening(CheckPlayerName):
    for Part in this.ListeningUsers:
        if Part[0] == CheckPlayerName:
            return True
    return False

def StartListenCommand(content, username, messageID, args, args2):
    print(this.ListeningUsers)
    if CheckListening(username) == False:
        print(username)
        print("GOVNONGUS = "+args)
        this.ListeningUsers.append([username, args])  # Добавляем пользователей в список с командой, которую они запросили.
        print(this.ListeningUsers)
        bot.sendMessage(ChannelId, IListenSay)
    else:
        bot.reply(ChannelId, messageID, "Хорошо, но я уже вас слушаю...")


def AddLimit(content, username, messageID, args, args2):
    print("ABOBAAAAAA")
    bot.reply(ChannelId, messageID, "сейчас...")
    retImage = get_asset_image.GetAssetImage(int(args2))
    variables.LIMITS.append(int(args2))
    ret = "Хорошо, лимитка `" + str(int(args2)) + "` - добавлена."
    bot.sendMessage(ChannelId, ret)
    bot.sendMessage(ChannelId, "Вот так она выглядит: "+retImage)
    ##bot.sendFile(ChannelId, retImage, True)
    print(3)
def ShowLimits(content, username, messageID, args, args2):
    print("ABOBAAAAAA")
    bot.reply(ChannelId, messageID, "сейчас...")
    if len(variables.LIMITS) > 0:
        text = ""
        for limit in variables.LIMITS:
            text = text + str(limit) + ", "
        text = text[:len(text)-2]
        ret = "Хорошо, вот все лимитки в моей базе данных которые я проверяю - `" + str(text) + "`"
        bot.sendMessage(ChannelId, ret)
    else:
        bot.sendMessage(ChannelId, "База данных лимиток пуста")

def DeleteLimit(content, username, messageID, args, args2):
    print("ABOBAAAAAA")
    bot.reply(ChannelId, messageID, "сейчас...")
    retImage = get_asset_image.GetAssetImage(int(args2))
    variables.LIMITS.remove(int(args2))
    ret = "Хорошо, лимитка `" + str(int(args2)) + "` - удалена."
    bot.sendMessage(ChannelId, ret)
    bot.sendMessage(ChannelId, "Вот так она выглядит: " + retImage)
def TurnOff(content, username, messageID, args, args2):
    print("ABOBAAAAAA")
    variables.PAUSE = False
    bot.reply(ChannelId, messageID, "Хорошо, сейчас вырублюсь.")
    bot.sendMessage(ChannelId, "Бот-BABUIN-UGC-Sniper прекращает свою работу(`отключение`).")
    sys.exit()

def Pause(content, username, messageID, args, args2):
    print("ABOBAAAAAA")
    variables.PAUSE = True
    bot.reply(ChannelId, messageID, "Хорошо, временно прекращаю проверку лимиток, чтобы возобновить скажите: `Бабуин -пауза`.")
def StopPause(content, username, messageID, args, args2):
    print("ABOBAAAAAA")
    variables.PAUSE = False
    bot.reply(ChannelId, messageID, "Хорошо, продолжаю проверку лимиток.")

def CheckItem(content, username, messageID, args, args2):
    print("ABOBAAAAAA")
    bot.reply(ChannelId, messageID, "сейчас...")
    retImage = get_asset_image.GetAssetImage(int(args2))
    bot.reply(ChannelId, messageID, "Вот так он выглядит': " + retImage)

this.BotStart = False
def StartWork(content, username, messageID, args, args2):
    if this.BotStart == False:
        print("ABOBAAAAAA")
        variables.PAUSE = False
        this.BotStart = True
        bot.reply(ChannelId, messageID, "Хорошо, сейчас начну проверку лимиток.")
        bot.sendMessage(ChannelId, "Бот-BABUIN-UGC-Sniper начинает проверку лимиток, а также быстрый их скуп в случае возможности купить.")
    else:
        print("ABOBAAAAAA")
        bot.reply(ChannelId, messageID, "Хорошо, но я и так веду проверку лимиток.")

# Functions
def CheckCommand(CommandName):  # ENGINE--
    for CN in this.Commands:
        print(CN[0] + " | " + CommandName)
        if (CN[0] == CommandName):
            if len(CN)>2:
                return CN[1], CN[2]
            else:
                return CN[1]
    return False

def GetUserActivatedCommand(UserName):  # ENGINE--
    for CN in this.ListeningUsers:
        print(CN[0] + " | " + UserName)
        if (CN[0] == UserName):
            if CN[1]:
                return CN[1]
    return False

@bot.gateway.command
def helloworld(resp):
    if resp.event.message:
        m = resp.parsed.auto()
        username = m['author']['username']
        messageID = m["id"]
        content = m['content'].split(":")[0]
        if len(m['content'].split(":")) > 1:
            args = m['content'].split(":")[1]
        else:
            args = ""
        if (username != BotUsername):
            print(username, BotUsername)
            Finded = CheckCommand(content)
            if (Finded and len(Finded)>0):
                Thread(target=globals()[Finded[0]], args=(content, username, messageID, Finded[1], args)).start()
            #else:
                #Command_ = GetUserActivatedCommand(username)
                #print("Hahaha: "+str(Command_))
                #Thread(target=globals()[Command_], args=(content, username, messageID, Command_)).start()

def StartCollect(ID):
    sayc = "ПРЕДМЕТ `" + str(int(ID)) + "` СТАЛ ДОСТУПНЫМ, НАЧИНАЮ СПАМИТЬ ЗАПРОСАМИ О ПОКУПКЕ!!!"
    Thread(target=bot.sendMessage, args=(ChannelId, sayc))
def DoneCollect(ID):
    sayc = "Поздравляю!!! Лимитированный предмет `"+str(int(ID))+"` был успешно добавлен в ваш инвентарь!"
    bot.sendMessage(ChannelId, sayc)
def DoneCollectWithError(ID):
    sayc = "Товар появился, однако произошла ЕБАНАЯ ошибка, но возможно, что предмет -`"+str(int(ID))+"`, все таки, успешно добавился в ваш инвентарь!"
    bot.sendMessage(ChannelId, sayc)

def START_BOT():
    print("START_BOT")
    # Function

    bot.sendMessage(ChannelId, HelpSay)

    bot.gateway.run(auto_reconnect=True)