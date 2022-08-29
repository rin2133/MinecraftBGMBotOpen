import discord
import ffmpeg
import youtube_dl
from discord.ext import commands
discord.opus.is_loaded()
TOKEN = 'プライバシーほご'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
voice = None
player = None
loopcom = 1

#引用しました。
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
#引用終了

#試験運用
url = 'https://www.youtube.com/watch?v=rJ2XfjqKJZk'

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
        #再生プログラム
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))


    if message.content == 'mcm!stop':
        if message.guild.voice_client is None:
            await message.channel.send('まだ再生していないよ！')
            return
        await message.channel.send('わかった。音楽を止めるね。')
        await message.guild.voice_client.disconnect()

client.run(TOKEN)
