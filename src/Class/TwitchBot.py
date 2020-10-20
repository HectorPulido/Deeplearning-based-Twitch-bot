from twitchio.ext import commands
from twitchio.webhook import UserFollows
import asyncio
import time
import random


class TwitchBot(commands.Bot):
    def __init__(
        self,
        client_secret,
        tmi_token,
        client_id,
        bot_nick,
        bot_prefix,
        channel,
        spam_message,
        default_messages,
        custom_events,
        custom_commands,
        time_to_spam=30,
        text_to_speech=None,
    ):
        """Deep learning based Twitch chatbot

        Args:
            client_secret (str): Client secret from twitch aplication
            tmi_token (str): Client tmi_token
            client_id (str): Client id
            bot_nick (str): Bot nickname
            bot_prefix (str): Bot command prefix
            channel (str): Channel to put the bot
            spam_message (dict): Spam events.
            default_messages (dict): Default messages.
            custom_events (dict): Events
            custom_commands (dict): commands
            time_to_spam (int, optional): Spam event launch time. Defaults to 30.
            text_to_speech (object, optional): .
        """
        self.viewer_list = []
        self.active = False

        self.client_secret = client_secret
        self.tmi_token = tmi_token
        self.client_id = client_id
        self.bot_nick = bot_nick
        self.bot_prefix = bot_prefix
        self.channel = channel
        self.time_to_spam = time_to_spam
        self.spam_message = spam_message
        self.default_messages = default_messages
        self.text_to_speech = text_to_speech

        self.custom_events = custom_events
        self.custom_commands = custom_commands

        super().__init__(
            client_secret=self.client_secret,
            irc_token=self.tmi_token,
            client_id=self.client_id,
            nick=self.bot_nick,
            prefix=self.bot_prefix,
            initial_channels=[self.channel],
        )

    async def event_ready(self):
        """On event ready"""

        print("Everything ready")
        self.channel_user = await self.get_users(
            self.channel.replace("#", "").lower().strip()
        )
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

        for event in self.custom_events:
            await event(message, self)

        await self.handle_custom_commands(message)

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
                chosen_item = random.choice(self.spam_message)
                await self._ws.send_privmsg(self.channel, chosen_item)

    async def event_raw_usernotice(self, channel, tags):
        """Responds to subs, resubs, raids and gifted subs"""

        if not self.active:
            return

        if tags["msg-id"] == "sub":
            message = self.default_messages["on_sub"].format(tags["display-name"])

        if tags["msg-id"] == "resub":
            message = self.default_messages["on_resub"].format(
                tags["display-name"], tags["msg-param-cumulative-months"]
            )

        if tags["msg-id"] == "raid":
            message = self.default_messages["on_raid"].format(tags["display-name"])

        if tags["msg-id"] == "subgift":
            message = self.default_messages["on_subgift"].format(tags["display-name"])

        if self.text_to_speech is not None:
            self.text_to_speech.say(message)

        await self._ws.send_privmsg(self.channel, message)

    async def handle_custom_commands(self, message):
        text = message.content.lower()
        for key, command in self.custom_commands.items():
            if text.startswith(self.bot_prefix + key.lower()):
                if type(command) is str:
                    return await message.channel.send(command)
                return await command(message, self)

    async def event_command_error(self, ctx, e):
        """ignore errors"""
        pass
