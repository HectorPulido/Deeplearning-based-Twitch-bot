import random

on_wet = "@{} le ha echado awa a @{}"

async def wet(message, bot):
    text = message.content.strip().split(" ")

    author = message.author.name

    if len(text) == 1:
        weated = random.choice(bot.viewer_list)
    else:
        weated = text[1].replace("@", "")

    await message.channel.send(on_wet.format(author, weated))