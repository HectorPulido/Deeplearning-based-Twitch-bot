on_bits = "Muchisimas gracias @{} por esos {} bits",

async def bit_message(message, bot):
    bits = message.tags.get("bits", None)

    if bits == None:
        return

    response = bot.default_messages["on_bits"] \
        .format(message.author.name, bits)
        
    await message.channel.send(response)