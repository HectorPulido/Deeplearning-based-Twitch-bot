class BitMessage:
    def __init__(self, on_bits_message, tts=None):
        self.tts = tts
        self.on_bits_message = on_bits_message

    async def __call__(self, message, _):
        if message.author is None:
            return

        bits = message.tags.get("bits", None)

        if bits is None:
            return

        response = self.on_bits_message

        response = response.replace("{user}", message.author.name)
        response = response.replace("{bits}", bits)

        if self.tts is not None:
            self.tts.say(response)

        await message.channel.send(response)
