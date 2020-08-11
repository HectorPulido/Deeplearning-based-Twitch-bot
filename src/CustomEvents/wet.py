import random

no_one_to_wet = "No existe tal usuario asi que te mojas a ti mismo @{}"
on_wet = "@{} le ha echado awa a @{}"

async def wet(message, bot):
    text = message.content.strip().split(" ")

    author = message.author.name

    if len(text) == 1:
        weated = random.choice(bot.viewer_list)
    else:
        weated = text[1].replace("@", "")

    if weated.lower() not in bot.viewer_list:
        return await message.channel.send(
            no_one_to_wet.format(author))

    await message.channel.send(on_wet.format(author, weated))