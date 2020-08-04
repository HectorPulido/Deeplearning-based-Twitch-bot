from twitchio.ext import commands
from twitchio.webhook import UserFollows
import asyncio
import time
import random


class TwitchBot(commands.Bot):

    def __init__(self,
                 chatbot,
                 client_secret,
                 tmi_token,
                 client_id,
                 bot_nick,
                 bot_prefix,
                 channel,
                 links_dict,
                 spam_message,
                 default_messages,
                 blacklist,
                 time_to_spam=30):
        """Deep learning based Twitch chatbot

        Args:
            chatbot (ChatbotBrain): Chatbot deep learning core
            client_secret (str): Client secret from twitch aplication
            tmi_token (str): Client tmi_token
            client_id (str): Client id
            bot_nick (str): Bot nickname
            bot_prefix (str): Bot command prefix
            channel (str): Channel to put the bot
            links_dict (dict): Bot links.
            spam_message (dict): Spam events.
            default_messages (dict): Default messages.
            blacklist (dict): prohibited words
            custom_events (dict): Events
            time_to_spam (int, optional): Spam event launch time. Defaults to 30.
        """

        self.chatbot = chatbot
        self.client_secret = client_secret
        self.tmi_token = tmi_token
        self.client_id = client_id
        self.bot_nick = bot_nick
        self.bot_prefix = bot_prefix
        self.channel = channel
        self.viewer_list = []
        self.active = False
        self.time_to_spam = time_to_spam
        self.links_dict = links_dict
        self.spam_message = spam_message
        self.default_messages = default_messages
        self.blacklist = blacklist

        super().__init__(
            client_secret=self.client_secret,
            irc_token=self.tmi_token,
            client_id=self.client_id,
            nick=self.bot_nick,
            prefix=self.bot_prefix,
            initial_channels=[self.channel]
        )

    async def event_ready(self):
        """On event ready
        """

        print("Everything ready")
        self.channel_user = await self.get_users(self.channel.replace("#", "").lower().strip())
        self.bot_user = await self.get_users(self.bot_nick.lower().strip())

        self.channel_user = self.channel_user[0]
        self.bot_user = self.bot_user[0]

        # run spam loop
        await self.spam_messages(self.time_to_spam)

    async def event_message(self, message):
        """Runs every time a message is sent in chat.

        Args:
            message (context): Message object containing relevant information.
        """
        await self.set_active(message)

        if not self.active:
            return

        # make sure the bot ignores itself
        if message.author.name.lower() == self.bot_nick.lower():
            return

        await self.welcome_message(message)
        await self.bit_message(message)
        await self.talk_to_bot(message)
        await self.handle_commands(message)

    async def bit_message(self, message):
        bits = message.tags.get("bits", None)

        if bits == None:
            return

        response = self.default_messages["on_bits"] \
            .format(message.author.name, bits)
        print(response)
        # await message.channel.send(response)

    async def welcome_message(self, message):
        if message.author.name.lower() in self.viewer_list:
            return

        self.viewer_list.append(message.author.name.lower())

        response = self.default_messages["welcome"] \
            .format(message.author.name)
        await message.channel.send(response)

    async def talk_to_bot(self, message):
        if f"@{self.bot_nick.lower()}" not in message.content.lower() + " EOL":
            return

        message_replaced = message.content.replace(f"@{self.bot_nick}", "")
        response = self.process_response(message_replaced)
        await message.channel.send(f"{response} @{message.author.name}")

    async def set_active(self, message):
        """Toggle bot active

        Args:
            active (bool): if the bot is not active, it'll no talk
        """

        if message.author.name.lower() not in self.channel.lower():
            return

        if "deactivatebot" in message.content + " EOL":
            self.active = False
            await message.channel.send(self.default_messages["on_deactivate"])
        elif "activatebot" in message.content + " EOL":
            self.active = True
            await message.channel.send(self.default_messages["on_active"])

    async def spam_messages(self, time_to_spam):
        """Repetitive messages

        Args:
            time_to_spam (int): time to repeat
        """

        while True:
            await asyncio.sleep(time_to_spam)

            if self.active:
                chosen_item = self.spam_message[random.randint(
                    0, len(self.spam_message) - 1)]

                ws = self._ws
                await ws.send_privmsg(self.channel, chosen_item)

    async def event_raw_usernotice(self, channel, tags):
        """Responds to subs, resubs, raids and gifted subs"""

        if not self.active:
            return

        ws = self._ws
        if tags["msg-id"] == "sub":
            message = self.default_messages["on_sub"].format(
                tags["display-name"])
            await ws.send_privmsg(self.channel, message)

        if tags["msg-id"] == "resub":
            message = self.default_messages["on_resub"].format(
                tags["display-name"],
                tags["msg-param-cumulative-months"]
            )
            await ws.send_privmsg(self.channel, message)

    async def event_command_error(self, ctx, e):
        """ignore errors"""
        pass

    def process_response(self, text):
        """Process the text of the command

        Args:
            text (str): Command text

        Returns:
            str: Talk response
        """

        text = text.lower()

        for blacklist_word in self.blacklist:
            if blacklist_word.lower() in text:
                return self.default_messages["blacklist"]

        for key, value in self.links_dict.items():
            if key.lower() in text:
                return self.default_messages["link"].format(key, value)

        return self.chatbot.talk(text)
