import random

duel_response = [
    "{winner} le corta la cabeza a {loser} y la usa como balon",
    "a {loser} le cayo una piedra gigante en la cabeza",
    "{winner} le lanza un cuchillo a {loser} y este lo esquiva pero, \
        se resvala y cae por el barranco",
    "{loser} salio corriendo de miedo, pero no se ató las agujetas y exploto",
    "{loser} maqueo y se auto disparo",
    "En el ultimo momento {winner} estaba arrinconado, todo estaba perdido, \
        pero luego le rezó al dios pequeñin y este bajo del cielo para darle \
        sus madrazos a {loser}",
    "Ya sin esperanza todos sabiamos que {loser} iba a morir... teniamos razon",
    "{loser} lanzó una roca y le cayó a el mismo",
    "{loser} saco a su Charizard nivel 100, pero esta mierda no es digimon, \
        el poder de la amistad no existe, y este se lo comio vivo",
    "a {loser} lo atropelló un tren antes de llegar al lugar de encuentro",
    "{loser} se ahogo con sus propias palabras",
    "{loser} esta confundido, perdedor se ha golpeado a si mismo multiples \
        veces hasta morir... pero murio de herpes"
]

no_duelist_message = "No has elegido contrincante, asi que tu enemigo será @{}"
self_duelist_message = "No puedes competir contra ti mismo"
no_existing_user_message = "El combatiente @{} no existe en este chat"
duel_start_message = "Empieza la pelea entre @{duelist_1} y @{duelist_1}"


async def duel(message, bot):
    text = message.content.strip().split(" ")

    duelist_1 = message.author.name

    if len(text) == 1:
        duelist_2 = random.choice(bot.viewer_list)
        await message.channel.send(no_duelist_message.format(duelist_2))
    else:
        duelist_2 = text[1].replace("@", "")

    if duelist_1.lower() == duelist_2.lower():
        return await message.channel.send(self_duelist_message)

    if duelist_2.lower() not in bot.viewer_list:
        return await message.channel.send(
            no_existing_user_message.format(duelist_2))

    await message.channel.send(duel_start_message.format(
        duelist_1=duelist_1, duelist_2=duelist_2))

    loser, winner = duelist_1, duelist_2

    if random.random() > 0.5:
        winner, loser = duelist_1, duelist_2

    duel_message = random.choice(duel_response).format(
        loser=loser, winner=winner)

    await message.channel.send(duel_message)
