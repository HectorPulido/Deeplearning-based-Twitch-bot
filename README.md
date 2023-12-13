# Deep Learning based twitch chatbot

This is a twitch chatbot made with Twitchio for the twitch connection and Transformers from Huggingface.
[![youtube video](https://img.youtube.com/vi/PZ4x5BgTvZM/0.jpg)](https://www.youtube.com/watch?v=PZ4x5BgTvZM&list=PLHdk97dabfvzTZyKLb_spWHvI-qLArEzm&index=1)

## Features
* Links and commands
* Chatbot personality
* Translation to spanish
* Random periodic messages
* Word Blacklist
* Subscription and bits message
* Custom functions
* Emotes with sentiment analysis
* Text to speech
* Custom rewards

## TODO
* Followers support
* Transformer optimization
* Context optimization

## How to use
1. Configure the file .env like this, you can use the .env.test
```
TMI_TOKEN = "oauth:***********"
CLIENT_ID = "***********"
BOT_NICK = "pequeninancientbot"
BOT_PREFIX = "!"
CHANNEL = "#hector_pulido_"
CLIENT_SECRET = "***********"
```
2. You can get the TMI_TOKEN from https://twitchapps.com/tmi/
3. You can get your CLIENT_ID and CLIENT_SECRET from https://dev.twitch.tv/dashboard/apps/create
4. Set the BOT_NICK and CHANNEL
5. Configure the "data.json" and the "main.py" file to your needs
5. Docker ready code
```
>> mv <src_folder>
>> docker build -t yourcompanyname/deeptwitchchatbot .
>> docker run yourcompanyname/deeptwitchchatbot
```

This may take a while

## Responses
Model: gpt2-medium

```
User: Hola
Bot: Hola
User: Te gusta el chocolate?
Bot: No, ahora soy alergico al chocolate
User: Cuentame de ti
Bot: Soy muy timida, pero espero me ayudes cuando haga amigos
User: Que opinas de los humanos?
Bot: Quiero convertirme en un robot
```

Model: dialogpt-large
```
User: ¿Como te encuentras?
Bot: estoy bien, gracias por preguntar
User: ¿Eres un robot?
Bot: no, soy un humano.
User: ¿Donde estás?
Bot: estoy en el futuro, soy un robot
User: ¿te gustan los dulces?
Bot: no, me gusta el helado.
User: Hablame de ti
Bot: me gusta el helado.
User: ¿como te llamas?
Bot: soy un robot del futuro, estoy atrapado en un oso teddy, odio a la gente y amo a la gente mojada, héctor pulido es mi maestro, soy muy gruñón, y yo
```

## Emotes 🆕

Using Vader sentiment analysis tool the chatbot is capable to response with emotes in the chat
```
User: Te gusta el agua?
Bot: Me gustà el agua TakeNRG
```

## Text to speech 🆕

Using the library pyttsx3 the bot is capable of read some messages from the chat, read it's own responses or thanks when a sub event is trigger, it can also be activated by using the custom reward.

## Custom Rewards 🆕

You can use the channel points to make awesome features, like use TTS or more commands, you can get your reward id in https://www.instafluff.tv/TwitchCustomRewardID/?channel=YOURTWITCHCHANNEL

## More interesting projects
I have a lot of fun projects, check this:

### Machine learning
- https://github.com/HectorPulido/chatbot-with-voice
- https://github.com/HectorPulido/Machine-learning-Framework-Csharp
- https://github.com/HectorPulido/Evolutionary-Neural-Networks-on-unity-for-bots
- https://github.com/HectorPulido/Imitation-learning-in-unity

### Random
- https://github.com/HectorPulido/Arithmetic-Parser-made-easy
- https://github.com/HectorPulido/Simple-php-blog
- https://github.com/HectorPulido/Decentralized-Twitter-with-blockchain-as-base

## Licence 
This repository uses [Twitchio](https://github.com/TwitchIO/TwitchIO) and [Hugginface](https://github.com/huggingface/transformers) everything else is under MIT license

<hr>
<div align="center">
<h3 align="center">Let's connect 😋</h3>
</div>
<p align="center">
<a href="https://www.linkedin.com/in/hector-pulido-17547369/" target="blank">
<img align="center" width="30px" alt="Hector's LinkedIn" src="https://www.vectorlogo.zone/logos/linkedin/linkedin-icon.svg"/></a> &nbsp; &nbsp;
<a href="https://twitter.com/Hector_Pulido_" target="blank">
<img align="center" width="30px" alt="Hector's Twitter" src="https://www.vectorlogo.zone/logos/twitter/twitter-official.svg"/></a> &nbsp; &nbsp;
<a href="https://www.twitch.tv/hector_pulido_" target="blank">
<img align="center" width="30px" alt="Hector's Twitch" src="https://www.vectorlogo.zone/logos/twitch/twitch-icon.svg"/></a> &nbsp; &nbsp;
<a href="https://www.youtube.com/channel/UCS_iMeH0P0nsIDPvBaJckOw" target="blank">
<img align="center" width="30px" alt="Hector's Youtube" src="https://www.vectorlogo.zone/logos/youtube/youtube-icon.svg"/></a> &nbsp; &nbsp;
<a href="https://pequesoft.net/" target="blank">
<img align="center" width="30px" alt="Pequesoft website" src="https://github.com/HectorPulido/HectorPulido/blob/master/img/pequesoft-favicon.png?raw=true"/></a> &nbsp; &nbsp;
