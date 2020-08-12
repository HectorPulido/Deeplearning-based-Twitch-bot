from Class.ChatbotBrain import ChatbotBrain
from Class.TwitchBot import TwitchBot
from CustomEvents.bit_message import bit_message
from CustomEvents.duel import duel
from CustomEvents.welcome import welcome
from CustomEvents.wet import wet
from CustomEvents.pick_random_user import pick_random_user
from CustomEvents.links import links
from CustomEvents.TalkToChatbot import TalkToChatbot
import secret

context = """who are you?
My name is Pequenin, I'm a robot from the future, I'm trapped \
in a teddy bear, I hate people and I love to wet people, Hector \
Pulido is my master, I am very grumpy, and I'm in the Hector twitch chat"""

translation_artifacts_english = {
    "Disagreement": "Discord"
}

translation_artifacts_spanish = {
    "pequenina": "Pequeñin",
    "osito de peluche": "Oso Teddy",
    "profesor": "Maestro"
}
chatbot = ChatbotBrain(context, translation_artifacts_english,
                       translation_artifacts_spanish, "microsoft/DialoGPT-large",
                       "microsoft/DialoGPT-large", True, True)

#from Class.TestChatbotBrain import TestChatbotBrain
#chatbot = TestChatbotBrain()

word_blacklist = [
    "nazi",
    "homosex",
    "judio",
    "comunis",
    "porn",
    "pedofi",
    "hitler",
    "guerra",
    "antisem"
]
blacklist_message = "No puedo responder a eso"
emotes = {
    "positive": ["❤", "😂", "😁", "😋", "TakeNRG", "VoHiYo"],
    "negative": ["😣", "😥", "🙁", "😰", "WutFace", "TheThing"]
}
talk_to_chatbot = TalkToChatbot(chatbot, word_blacklist, blacklist_message, emotes)

custom_events = [bit_message, welcome, links, talk_to_chatbot]
custom_commands = {
    "duelo": duel,
    "mojar": wet,
    "pickoneuser": pick_random_user
}

spam_message = [
    "¡Suscribete a nuestro canal de youtube para enterarte \
    de lo ultimo de desarrollo de videojuegos e inteligencia \
    artificial! https://www.youtube.com/c/hectorandrespulidopalmar",
    "Te invito a nuestro grupo de discord, https://discord.gg/ZsUpJJc, \
    siempre hablamos de cosas interesantes",
    "Sigue a Hector en Twitter, dice puras pendejadas, pero pendejadas \
    interesantes https://twitter.com/Hector_Pulido_",
    "¿Quieres saber como estoy hecho? entra a el github: \
    https://github.com/HectorPulido",
    "Recuerda que si le picas al follow twitch te avisará de los proximos \
    directos",
    "Habla conmigo tageandome, no seas timido, pregunta lo que quieras",
    "Recuerda que si tienes Twitch prime, la suscripcion es gratis <3"
    # "No te olvides de seguir a nuestros amigos de aventuras en carreta https://twitter.com/avent_carreta",
    # "No te olvides de seguir a @cadstor_val https://twitter.com/Val_Castor_",
    # "No te olvides de seguir a el jeñor puni (y echarle awa) https://twitter.com/puni_xa",
    # "No te olvides de seguir a la master Mey https://twitter.com/Zaix64713153",
]

default_messages = {
    "on_active": "Circulo de invocacion completo, Fui invocado del mas allá!",
    "on_deactivate": "Bot desactivado",
    "on_sub": "Muchisimas gracias @{} por ese sub, bienvenid@ a la familia <3",
    "on_resub": "Muchisimas gracias @{} por esa re sub, ¡{} meses WOW! que \
        alegria tenerte de nuevo por aqui <3",
    "on_raid": "Muchas gracias por ese raid @{}, bienvenidos todos <3",
    "on_subgift": "Muchisimas gracias @{} por regalar esas subs <3"
}
TIME_TO_SPAM = 60 * 10
bot = TwitchBot(secret.CLIENT_SECRET, secret.TMI_TOKEN, secret.CLIENT_ID,
                secret.BOT_NICK, secret.BOT_PREFIX, secret.CHANNEL, spam_message,
                default_messages, custom_events, custom_commands, TIME_TO_SPAM)


if __name__ == "__main__":
    bot.run()
