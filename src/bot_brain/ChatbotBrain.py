import re
import logging
from gpt4all import GPT4All
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class ChatbotBrain:
    def __init__(
        self,
        info,
        translator=None,
    ):
        """This is a deep learning chatbot with traduction

        Args:
            info (dict): Chatbot info
            translator (object, optional): Translator object. Defaults to None.
        """

        self.generator = GPT4All(info["model"])
        self.sentiment_analisis = info["sentiment_analisis"]
        self.max_tokens = info["max_tokens"]
        self.temperature = info["temperature"]
        self.translator = translator

        prompt = open(info["prompt"], "r", encoding="utf-8")
        self.prompt = str(prompt.read())
        logging.debug("Loading prompt")
        logging.debug("Prompt: %s", self.prompt)

        self.temporal_context = []

        if self.sentiment_analisis:
            self.sentiment_engine = SentimentIntensityAnalyzer()

    def post_process_text(self, ask):
        """Post process the response to avoid links

        Args:
            ask (str): response string

        Returns:
            str: post processed response string
        """
        ask = ask.strip()
        search = re.findall(r"(([A-Z0-9]+\.)+[A-Z0-9]+)", ask, flags=re.IGNORECASE)
        for match in search:
            ask = ask.replace(match[0], "")

        ask = re.sub(r"\W+\?\!\.\,", "", ask)
        return ask[:300]

    def get_sentiment(self, text):
        """Get sentiment of a text
        Args:
            text (text):

        Returns:
            float: sentiment
        """
        return self.sentiment_engine.polarity_scores(text)["compound"]

    def talk(self, ask):
        """Talk to the chatbot

        Args:
            ask (string): Text to talk with the chatbot

        Returns:
            string: Chatbot response
            float: Response sentiment
        """
        # Process text
        ask = self.post_process_text(ask)

        # Translate to english
        if self.translator is not None:
            ask = self.translator.spanish_to_english(ask)

        self.temporal_context.append(ask)
        ask = self.prompt.replace("{input}", ask)

        logging.debug("========= Prompt =========")
        logging.debug("Prompt: %s", ask)
        logging.debug("==========================")

        # TODO add context

        # Generate text and parse data
        generated_text = self.generator.generate(
            ask, max_tokens=self.max_tokens, temp=self.temperature
        )
        generated_text = self.post_process_text(generated_text)

        # Sentiment
        if self.sentiment_analisis:
            sentiment = self.get_sentiment(generated_text)

        # Add response to context
        self.temporal_context.append(generated_text)

        # Translate to spanish
        if self.translator is not None:
            generated_text = self.translator.english_to_spanish(generated_text)

        if self.sentiment_analisis:
            return generated_text, sentiment

        return generated_text
