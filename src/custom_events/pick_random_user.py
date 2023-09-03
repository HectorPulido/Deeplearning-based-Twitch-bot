import random

choosen_text = "El elegido es @{}"


async def pick_random_user(message, bot):
    choosen = random.choice(bot.viewer_list)
    await message.channel.send(choosen_text.format(choosen))
