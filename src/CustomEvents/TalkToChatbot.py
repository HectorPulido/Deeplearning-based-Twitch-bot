import random


class TalkToChatbot:
    def __init__(self, chatbot, blacklist, blacklist_message, emotes=None, tts=None):
        self.chatbot = chatbot
        self.blacklist = blacklist
        self.blacklist_message = blacklist_message
        self.emotes = emotes
        self.tts = tts

    async def __call__(self, message, bot):
        if f"@{bot.bot_nick.lower()}" not in message.content.lower() + " EOL":
            return

        message_replaced = message.content.replace(f"@{bot.bot_nick}", "").lower()

        if self.check_blacklist(message_replaced):
            return await message.channel.send(self.blacklist_message)

        response = self.process_response(message_replaced)

        if self.emotes is not None and type(response) is tuple:
            text, sentiment = response
            response = text + " " + self.get_emote(sentiment)

        if self.tts is not None:
            self.tts.say(response + " " + message.author.name)

        await message.channel.send(f"{response} @{message.author.name}")

    def get_emote(self, sentiment):
        if sentiment > 0.2:
            emote = random.choice(self.emotes["positive"])
        elif sentiment < -0.2:
            emote = random.choice(self.emotes["negative"])
        else:
            emote = random.choice(self.emotes["neutral"])

        return emote

    def check_blacklist(self, text):
        for blacklist_word in self.blacklist:
            if blacklist_word.lower() in text:
                return True
        return False

    def process_response(self, text):
        """Process the text of the command

        Args:
            text (str): Command text

        Returns:
            str: Talk response
        """
        return self.chatbot.talk(text)
