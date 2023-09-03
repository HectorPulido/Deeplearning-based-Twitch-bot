import pyttsx4
import logging
from sys import platform

# MAC OS
if platform == "darwin":
    from os import system


class TextToSpeech:
    def __init__(self, info):
        self.template = info["template"]
        self.tts_active = True
        if platform != "darwin":
            self.engine = pyttsx4.init("nsss")
            self.engine.setProperty("rate", float(info["rate"]))
        self.say("Text to speech activated")
        logging.debug("Text to speech activated")

    async def __call__(self, message, bot):
        if message.author is None:
            return
        text = message.content
        author = message.author.name
        self.check_activate(text, author, bot)
        self.say(self.template.format(user=author, text=text))

    def say(self, text):
        if not self.tts_active:
            return

        if text is None:
            return

        # MAC OS
        if platform == "darwin":
            system('say -v "Mónica" ' + text)
            return

        self.engine.say(text)
        self.engine.runAndWait()

    def check_activate(self, text, author, bot):
        if author.lower() != bot.channel.replace("#", "").lower():
            return

        if text == "activatetts":
            self.tts_active = True
            return

        if text == "deactivatetts":
            self.tts_active = False
