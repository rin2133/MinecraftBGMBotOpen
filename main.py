import discord
import ffmpeg
import youtube_dl
from discord.ext import commands
discord.opus.is_loaded()
TOKEN = 'MTAxMzIzMjU2Nzg0OTMzNjkyMw.Gzx7yn.pFLSft-D9JOlTLUreowOaNleXSnbjW6bjN1BAw'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
voice = None
player = None
loopcom = 1


@client.event
async def on_ready():
    print('Enter Sucsess')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content == '/test':
        await message.channel.send('OK TEST')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    global voice,player
    
    if message.content == 'mcm!play':
        if message.author.voice is None:
            await message.channel.send('ボイスチャンネルに入ってからもう一回試してみて！')
            return
        await message.author.voice.channel.connect()
        await message.channel.send('音楽を再生したよ！！')
    
    if message.content == 'mcm!stop':
        if message.guild.voice_client is None:
            await message.channel.send('まだ再生していないよ！')
            return
        await message.channel.send('わかった。音楽を止めるね。')
        await message.guild.voice_client.disconnect()

client.run(TOKEN)