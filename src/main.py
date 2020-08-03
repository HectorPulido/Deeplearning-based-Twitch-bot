from Class.ChatbotBrain import ChatbotBrain
from Class.TwitchBot import TwitchBot
import secret

if __name__ == "__main__":
    chatbot = ChatbotBrain()
    bot = TwitchBot(chatbot, secret.CLIENT_SECRET, secret.TMI_TOKEN, secret.CLIENT_ID,
                    secret.BOT_NICK, secret.BOT_PREFIX, secret.CHANNEL, 60)
    bot.run()

