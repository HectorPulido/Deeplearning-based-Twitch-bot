import os
import json
import logging
from dotenv import load_dotenv
from bot_brain import ChatbotBrain, TwitchBot, Translator, TestChatbotBrain
from custom_events import (
    duel,
    welcome,
    wet,
    links,
    BitMessage,
    TalkToChatbot,
    TextToSpeech,
)

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="w",
    format="%(asctime)s -%(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

load_dotenv()

CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TMI_TOKEN = os.getenv("TMI_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
BOT_NICK = os.getenv("BOT_NICK")
CHANNEL = os.getenv("CHANNEL")
TESTING = os.getenv("TESTING") == "TRUE"


if __name__ == "__main__":
    with open("data.json", "r", encoding="utf-8") as config:
        data = json.load(config)

        if TESTING:
            chatbot = TestChatbotBrain()
        else:
            translator = None
            if "translation" in data:
                translator = Translator(data["translation"])
            chatbot = ChatbotBrain(data["bot"], translator)

        text_to_speech = TextToSpeech(data["text_to_speech"])

        talk_to_chatbot = TalkToChatbot(
            chatbot, data["word_blacklist"], data["blacklist_message"], data["emotes"]
        )
        bit_message = BitMessage(data["on_bits"], text_to_speech)

        custom_events = [bit_message, welcome, links, talk_to_chatbot]

        custom_commands = data["custom_commands"]
        spam_message = data["spam_message"]
        default_messages = data["default_messages"]

        custom_rewards = data["custom_rewards"]
        custom_rewards["e2665151-3aef-4add-8292-1223d27fb671"] = text_to_speech
        custom_rewards["a48e6dbc-bdd6-4492-b460-027642f48c02"] = wet
        custom_rewards["fbfa5734-9d04-482d-8d3d-177b4e574861"] = duel

        time_to_spam = data["time_to_spam"]

        bot_prefix = data["bot_prefix"]

        logging.debug("Starting bot")
        TIME_TO_SPAM = data["time_to_spam"]
        bot = TwitchBot(
            CLIENT_SECRET,
            TMI_TOKEN,
            CLIENT_ID,
            BOT_NICK,
            bot_prefix,
            CHANNEL,
            spam_message,
            default_messages,
            custom_events,
            custom_commands,
            custom_rewards,
            TIME_TO_SPAM,
            text_to_speech,
        )
        bot.run()
