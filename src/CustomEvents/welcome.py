welcome_message = "Bienvenid@ al stream, ¡ @{} !"


async def welcome(message, bot):
    if message.author.name in bot.viewer_list:
        return

    bot.viewer_list.append(message.author.name)

    response = welcome_message.format(message.author.name)

    await message.channel.send(response)
