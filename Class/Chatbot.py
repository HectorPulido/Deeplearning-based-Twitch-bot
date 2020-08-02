from transformers import pipeline, set_seed, MarianMTModel, MarianTokenizer


class chatbot:
    context = """
User: Hi who are you?
Pequenin: I'm pequenin a robot from the future
User: Discord server
Pequenin: https://discord.gg/ZsUpJJc
User: do you like people?
Pequenin: no, i hate people
User: Who is your master
Pequenin: My master is Hector Pulido
User: How do you look?
Pequenin: I look like a teddy bear
User: Where are you right now?
Pequenin: I'm in Hector's twitch chat
User: {}
Pequenin:"""

    traduction_artifacts_english = {
        "Disagreement": "Discord"
    }

    traduction_artifacts = {
        "pequenina": "Pequeñin",
        "osito de peluche": "Oso Teddy",
        "profesor": "Maestro"
    }

    def __init__(self, seed=44):
        self.generator = pipeline(
            'text-generation', model='distilgpt2', tokenizer='distilgpt2')

        # ENG -> SPANISH
        self.model_name_EN_T_ES = 'Helsinki-NLP/opus-mt-en-ROMANCE'
        self.tokenizer_EN_T_ES = MarianTokenizer.from_pretrained(
            self.model_name_EN_T_ES)
        self.model_EN_T_ES = MarianMTModel.from_pretrained(
            self.model_name_EN_T_ES)

        # ESP -> ENGLISH
        self.model_name_ES_T_EN = 'Helsinki-NLP/opus-mt-ROMANCE-en'
        self.tokenizer_ES_T_EN = MarianTokenizer.from_pretrained(
            self.model_name_ES_T_EN)
        self.model_ES_T_EN = MarianMTModel.from_pretrained(
            self.model_name_ES_T_EN)

        set_seed(seed)

    def english_to_spanish(self, text):
        src_text = ['>>es<< {}'.format(text)]
        translated = self.model_EN_T_ES.generate(
            **self.tokenizer_EN_T_ES.prepare_translation_batch(src_text))
        tgt_text = [self.tokenizer_EN_T_ES.decode(
            t, skip_special_tokens=True) for t in translated]
        return tgt_text[0]

    def spanish_to_english(self, text):
        src_text = [text]
        translated = self.model_ES_T_EN.generate(
            **self.tokenizer_ES_T_EN.prepare_translation_batch(src_text))
        tgt_text = [self.tokenizer_ES_T_EN.decode(
            t, skip_special_tokens=True) for t in translated]
        return tgt_text[0]

    def replace_traduction_artifacts_en_sp(self, text):
        for word, initial in self.traduction_artifacts.items():
            text = text.lower().replace(word.lower(), initial.lower())
        return text

    def replace_traduction_artifacts_sp_en(self, text):
        for word, initial in self.traduction_artifacts_english.items():
            text = text.lower().replace(word.lower(), initial.lower())
        return text

    def ask_pequenin(self, ask):
        ask = self.spanish_to_english(ask)
        ask = self.replace_traduction_artifacts_sp_en(ask)

        self.context = self.context.format(ask)

        data = self.generator(self.context, max_length=int(len(self.context)))
        data = data[0]["generated_text"]
        data = data.replace(self.context, "")
        data = data.split("\n")[0].strip()

        data = self.replace_traduction_artifacts_en_sp(data)

        self.context += data + "\n"
        self.context += "User: {}\n"
        self.context += "Pequenin:"

        return self.english_to_spanish(data)
