import sched, time, random
from twitchio.ext import commands
from secret import *
from Class.Chatbot import chatbot

pequenin = chatbot()

TIME_TO_SPAM = 10
viewer_list = []

# set up the bot
bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)

links_dict = {
    "youtube" : "https://www.youtube.com/c/hectorandrespulidopalmar",
    "discord" : "https://discord.gg/ZsUpJJc",
    "twitter" : "https://twitter.com/Hector_Pulido_",
    "github" : "https://github.com/HectorPulido"
}

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(CHANNEL, f"/LLegó del mas allá!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == BOT_NICK.lower():
        return

    await bot.handle_commands(ctx)

    if ctx.author.name not in viewer_list:
        viewer_list.append(ctx.author.name)
        await ctx.channel.send(f"Bienvenido al stream, @{ctx.author.name}!")
    
    if f"@{BOT_NICK}" in ctx.content + " EOL":
        response = process_response(ctx.content.replace(f"@{BOT_NICK}", ""))
        await ctx.channel.send(f"{response}, @{ctx.author.name}")
        

def spam(sc): 

    items = list(links_dict.items())
    chosed_item = items[random.randint(0, len(items) - 1)]

    ws = bot._ws
    ws.send_privmsg(CHANNEL, f"Unete a nuestro {chosed_item[0]}: {chosed_item[1]}!")

    # do your stuff
    s.enter(TIME_TO_SPAM, 2, spam, (sc,))

def process_response(text):
    for key, value in links_dict.items():
        if key in text:
            return f"Unete a nuestro {key}: {value}!"

    return pequenin.ask_pequenin(text)


if __name__ == "__main__":
    bot.run()
    # s = sched.scheduler(time.time, time.sleep)
    # s.enter(TIME_TO_SPAM, 2, spam, (s,))
    # s.run()