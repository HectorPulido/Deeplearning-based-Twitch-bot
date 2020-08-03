from transformers import pipeline, set_seed, MarianMTModel, MarianTokenizer


class ChatbotBrain:
    context = """
User: Hi who are you?
Bot: I'm pequenin a robot from the future
User: Discord server
Bot: https://discord.gg/ZsUpJJc
User: do you like people?
Bot: no, i hate people
User: Who is your master
Bot: My master is Hector Pulido
User: How do you look?
Bot: I look like a teddy bear
User: Where are you right now?
Bot: I'm in Hector's twitch chat
User: {}
Bot:"""

    translation_artifacts_english = {
        "Disagreement": "Discord"
    }

    translation_artifacts = {
        "pequenina": "Pequeñin",
        "osito de peluche": "Oso Teddy",
        "profesor": "Maestro"
    }

    def __init__(self,
                 context=None,
                 traduction_english_artifacts=None,
                 traduction_spanish_artifacts=None,
                 translate=True,
                 seed=44):
        """This is a deep learning chatbot with traduction

        Args:
            context (Chatbot): context
            traduction_english_artifacts (dict): Dictionary of artifacts
            traduction_spanish_artifacts (dict): Dictionary of artifacts
            translate (bool, optional): Input and output will be translated?. Defaults to True.
            seed (int, optional): random seed. Defaults to 44.
        """

        self.generator = pipeline(
            'text-generation',
            model='distilgpt2',
            tokenizer='distilgpt2')

        self.translate = translate

        if context is not None:
            self.context = context

        if traduction_english_artifacts is not None:
            self.translation_artifacts_english = traduction_english_artifacts

        if traduction_spanish_artifacts is not None:
            self.traduction_spanish_artifacts = traduction_spanish_artifacts

        set_seed(seed)

        if translate:
            # ENG -> SPANISH
            self.model_name_en_t_es = 'Helsinki-NLP/opus-mt-en-ROMANCE'
            self.tokenizer_en_t_es = MarianTokenizer.from_pretrained(
                self.model_name_en_t_es)
            self.model_en_t_es = MarianMTModel.from_pretrained(
                self.model_name_en_t_es)

            # ESP -> ENGLISH
            self.model_name_es_t_en = 'Helsinki-NLP/opus-mt-ROMANCE-en'
            self.tokenizer_es_t_en = MarianTokenizer.from_pretrained(
                self.model_name_es_t_en)
            self.model_es_t_en = MarianMTModel.from_pretrained(
                self.model_name_es_t_en)

    def english_to_spanish(self, text):
        """English to spanish translation

        Args:
            text (string): English text to be translated

        Returns:
            string: Translated text
        """

        src_text = ['>>es<< {}'.format(text)]
        translated = self.model_en_t_es.generate(
            **self.tokenizer_en_t_es.prepare_translation_batch(src_text))
        tgt_text = [self.tokenizer_en_t_es.decode(
            t, skip_special_tokens=True) for t in translated]
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
            **self.tokenizer_es_t_en.prepare_translation_batch(src_text))
        tgt_text = [self.tokenizer_es_t_en.decode(
            t, skip_special_tokens=True) for t in translated]
        return tgt_text[0]

    def replace_translation_artifacts_en_sp(self, text):
        """Replace the artifacts in the traduction with the setted words

        Args:
            text (string): Text to replace

        Returns:
            string: Replaced text
        """

        for word, initial in self.translation_artifacts.items():
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

    def talk(self, ask):
        """Talk to the chatbot

        Args:
            ask (string): Text to talk with the chatbot

        Returns:
            string: Chatbot response
        """

        if self.translate:
            ask = self.spanish_to_english(ask)
            ask = self.replace_translation_artifacts_sp_en(ask)

        self.context = self.context.format(ask)

        max_length = len(self.generator.tokenizer.encode(self.context)) + 10

        data = self.generator(self.context, max_length=max_length)
        data = data[0]["generated_text"]
        data = data.replace(self.context, "")
        data = data.split("\n")[0].strip()

        self.context += data + "\n"
        self.context += "User: {}\n"
        self.context += "Bot: "

        if self.translate:
            data = self.english_to_spanish(data)
            data = self.replace_translation_artifacts_en_sp(data)

        return data
