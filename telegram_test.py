import telegram, json

telgm_token = '1697466514:AAGpkhzP4WZTZi2ejxK3oTUU56Cs6b-NoCM'
id = '1169772729'

bot = telegram.Bot(token=telgm_token)
updates = bot.getUpdates()

for i in updates:
    print(i.message)

print('start telegram chat bot')

bot.sendMessage(chat_id=id, text="")