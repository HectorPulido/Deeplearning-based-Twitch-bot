link_text = "Siguenos en {}: {}"

links_dict = {
    "youtube": "https://www.youtube.com/c/hectorandrespulidopalmar",
    "discord": "https://discord.gg/ZsUpJJc",
    "twitter": "https://twitter.com/Hector_Pulido_",
    "github": "https://github.com/HectorPulido"
}


async def links(message, bot):
    text = message.content.lower()

    if f"@{bot.bot_nick.lower()}" not in text + " EOL":
        return
    
    for key, value in links_dict.items():
        if key.lower() in text:
            return link_text.format(key, value)
