no_one_to_wet = "No existe tal usuario asi que te mojas a ti mismo @{}"
on_wet = "@{} le ha echado awa a @{}"


async def wet(message, bot):
    if message.author is None:
        return
    author = message.author.name
    target = message.content.strip().split(" ")[0].replace("@", "")

    if target.lower() not in bot.viewer_list:
        return await message.channel.send(no_one_to_wet.format(author))

    await message.channel.send(on_wet.format(author, target))
