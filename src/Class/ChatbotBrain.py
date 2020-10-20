import re
from transformers import pipeline, set_seed, MarianMTModel, MarianTokenizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class ChatbotBrain:
    def __init__(
        self,
        context,
        translation_artifacts_english,
        translation_artifacts_spanish,
        model="microsoft/DialoGPT-small",
        tokenizer="microsoft/DialoGPT-small",
        translate=True,
        sentiment_analisis=False,
        seed=44,
    ):
        """This is a deep learning chatbot with traduction

        Args:
            context (Chatbot): context
            traduction_english_artifacts (dict): Dictionary of artifacts
            traduction_spanish_artifacts (dict): Dictionary of artifacts
            translate (bool, optional): Input and output will be translated?.
            seed (int, optional): random seed. Defaults to 44.
            sentiment_analisis (bool, optional):
        """

        self.generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

        self.translate = translate
        self.context = context
        self.translation_artifacts_english = translation_artifacts_english
        self.translation_artifacts_spanish = translation_artifacts_spanish
        self.sentiment_analisis = sentiment_analisis

        self.parsed_context = self.generator.tokenizer.eos_token.join(
            context.split("\n")
        )

        self.temporal_context = []

        set_seed(seed)

        if sentiment_analisis:
            self.sentiment_engine = SentimentIntensityAnalyzer()

        if translate:
            # ENG -> SPANISH
            self.model_name_en_t_es = "Helsinki-NLP/opus-mt-en-ROMANCE"
            self.tokenizer_en_t_es = MarianTokenizer.from_pretrained(
                self.model_name_en_t_es
            )
            self.model_en_t_es = MarianMTModel.from_pretrained(self.model_name_en_t_es)

            # ESP -> ENGLISH
            self.model_name_es_t_en = "Helsinki-NLP/opus-mt-ROMANCE-en"
            self.tokenizer_es_t_en = MarianTokenizer.from_pretrained(
                self.model_name_es_t_en
            )
            self.model_es_t_en = MarianMTModel.from_pretrained(self.model_name_es_t_en)

    def english_to_spanish(self, text):
        """English to spanish translation

        Args:
            text (string): English text to be translated

        Returns:
            string: Translated text
        """

        src_text = [">>es<< {}".format(text)]
        translated = self.model_en_t_es.generate(
            **self.tokenizer_en_t_es.prepare_seq2seq_batch(src_text)
        )
        tgt_text = [
            self.tokenizer_en_t_es.decode(t, skip_special_tokens=True)
            for t in translated
        ]
        return tgt_text[0]

    def spanish_to_english(self, text):
        """Spanish to english translation

        Args:
            text (string): Spanish text to be translated

        Returns:
            string: Translated text
        """

        src_text = [text]
        translated = self.model_es_t_en.generate(
            **self.tokenizer_es_t_en.prepare_seq2seq_batch(src_text)
        )
        tgt_text = [
            self.tokenizer_es_t_en.decode(t, skip_special_tokens=True)
            for t in translated
        ]
        return tgt_text[0]

    def replace_translation_artifacts_en_sp(self, text):
        """Replace the artifacts in the traduction with the setted words

        Args:
            text (string): Text to replace

        Returns:
            string: Replaced text
        """

        for word, initial in self.translation_artifacts_spanish.items():
            text = text.lower().replace(word.lower(), initial.lower())
        return text

    def replace_translation_artifacts_sp_en(self, text):
        """Replace the artifacts in the traduction with the setted words

        Args:
            text (string): Text to replace

        Returns:
            string: Replaced text
        """

        for word, initial in self.translation_artifacts_english.items():
            text = text.lower().replace(word.lower(), initial.lower())
        return text

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
        return ask[:500]

    def get_sentiment(self, text):
        """

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
        if self.translate:
            ask = self.spanish_to_english(ask)
            ask = self.replace_translation_artifacts_sp_en(ask)

        self.temporal_context.append(ask)

        # Set context: last 2 exchanges + first context
        parsed_temp_context = self.generator.tokenizer.eos_token.join(
            self.temporal_context[-3:]
        )
        context_input = self.generator.tokenizer.eos_token.join(
            [self.parsed_context, parsed_temp_context, ""]
        )

        # Get max content len
        max_length = len(self.generator.tokenizer.encode(context_input)) + 1000

        # Generate text and parse data
        generated_text = self.generator(context_input, max_length=max_length)
        generated_text = generated_text[0]["generated_text"].split(
            self.generator.tokenizer.eos_token
        )[-1]
        generated_text = self.post_process_text(generated_text)

        # Sentiment
        if self.sentiment_analisis:
            sentiment = self.get_sentiment(generated_text)

        # Add response to context
        self.temporal_context.append(generated_text)

        # Translate to spanish
        if self.translate:
            generated_text = self.english_to_spanish(generated_text)
            generated_text = self.replace_translation_artifacts_en_sp(generated_text)

        if self.sentiment_analisis:
            return generated_text, sentiment

        return generated_text
