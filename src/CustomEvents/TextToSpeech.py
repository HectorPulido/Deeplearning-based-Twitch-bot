import pyttsx3


class TextToSpeech:
    def __init__(self, template, rate=150):
        self.template = template
        self.tts_active = True
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)

    async def __call__(self, message, bot):

        text = message.content
        author = message.author.name
        self.check_activate(text, author, bot)
        self.say(self.template.format(author, text))

    def say(self, text):
        if not self.tts_active:
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
            return
