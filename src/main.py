from Class.ChatbotBrain import ChatbotBrain
from Class.TwitchBot import TwitchBot
import secret

context = """who are you?
My name is Pequenin, I'm a robot from the future, I'm trapped in a teddy bear, I hate people and I love to wet people, Hector Pulido is my master, I am very grumpy, and I'm in the Hector twitch chat"""

translation_artifacts_english = {
    "Disagreement": "Discord"
}

translation_artifacts_spanish = {
    "pequenina": "Pequeñin",
    "osito de peluche": "Oso Teddy",
    "profesor": "Maestro"
}

links_dict = {
    "youtube": "https://www.youtube.com/c/hectorandrespulidopalmar",
    "discord": "https://discord.gg/ZsUpJJc",
    "twitter": "https://twitter.com/Hector_Pulido_",
    "github": "https://github.com/HectorPulido"
}

spam_message = [
    "¡Suscribete a nuestro canal de youtube para enterarte \
    de lo ultimo de desarrollo de videojuegos e inteligencia \
    artificial! https://www.youtube.com/c/hectorandrespulidopalmar",
    "Te invito a nuestro grupo de discord, https://discord.gg/ZsUpJJc, \
    siempre hablamos de cosas interesantes"
    "Sigue a Hector en Twitter, dice puras pendejadas, pero pendejadas \
    interesantes https://twitter.com/Hector_Pulido_",
    "¿Quieres saber como estoy hecho? entra a el github: \
    https://github.com/HectorPulido",
    "Recuerda que si le picas al follow twitch te avisará de los proximos \
    directos",
    "Habla conmigo tageandome, no seas timido, pregunta lo que quieras",
    "Recuerda que si tienes Twitch prime, la suscripcion es gratis <3"
]

default_messages = {
    "on_init": "Circulo de invocacion completo",
    "on_active": "Fui invocado del mas allá!",
    "on_deactivate": "Bot desactivado",
    "welcome": "Bienvenido al stream, ¡@{}!",
    "link": "Siguenos en {}: {}"
}

if __name__ == "__main__":
    chatbot = ChatbotBrain(
        context, translation_artifacts_english, translation_artifacts_spanish)
    bot = TwitchBot(chatbot, secret.CLIENT_SECRET, secret.TMI_TOKEN, secret.CLIENT_ID,
                    secret.BOT_NICK, secret.BOT_PREFIX, secret.CHANNEL, links_dict, spam_message,
                    default_messages, 120)
    bot.run()
