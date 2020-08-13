class BitMessage:
    def __init__(self, on_bits_message, tts = None):
        self.tts = tts
        self.on_bits_message = on_bits_message

    async def __call__(self, message, bot):
        bits = message.tags.get("bits", None)

        if bits == None:
            return

        response = self.on_bits_message.format(message.author.name, bits)

        if self.tts is not None:
            self.tts.say(response)
            
        await message.channel.send(response)