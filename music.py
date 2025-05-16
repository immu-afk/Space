import discord
from discord.ext import commands
import wavelink

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.start_node())
        self.queue = {}

    async def start_node(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host='127.0.0.1',
            port=2333,
            password='youshallnotpass',
            region='us_central'
        )

    def get_queue(self, guild):
        return self.queue.setdefault(guild.id, [])

    @commands.command()
    async def join(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("You must be in a voice channel to use this command.")

        channel = ctx.author.voice.channel
        player = wavelink.NodePool.get_node().get_player(ctx.guild)

        if not player.is_connected:
            await player.connect(channel.id)
            await ctx.send(f"Joined {channel.name}!")

    @commands.command()
    async def play(self, ctx, *, search: str):
        await self.join(ctx)
        player = wavelink.NodePool.get_node().get_player(ctx.guild)

        if "open.spotify.com" in search:
            tracks = await wavelink.SpotifyTrack.search(search)
        else:
            tracks = await wavelink.YouTubeTrack.search(search)

        if not tracks:
            return await ctx.send("No tracks found.")

        track = tracks[0]
        queue = self.get_queue(ctx.guild)
        queue.append(track)
        await ctx.send(f"Added to queue: {track.title}")

        if not player.is_playing:
            await self.start_playback(ctx, player)

    async def start_playback(self, ctx, player):
        queue = self.get_queue(ctx.guild)
        if not queue:
            return

        track = queue.pop(0)
        await player.play(track)
        await ctx.send(f"Now playing: {track.title}")

    @commands.command()
    async def pause(self, ctx):
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        if player.is_playing:
            await player.pause()
            await ctx.send("Paused playback.")

    @commands.command()
    async def resume(self, ctx):
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        if player.is_paused:
            await player.resume()
            await ctx.send("Resumed playback.")

    @commands.command()
    async def skip(self, ctx):
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        await ctx.send("Skipped track.")
        await self.start_playback(ctx, player)

    @commands.command()
    async def stop(self, ctx):
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        await player.disconnect()
        self.queue[ctx.guild.id] = []
        await ctx.send("Stopped and cleared queue.")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload):
        player = payload.player
        guild = player.guild
        ctx = await self.bot.get_context(guild.system_channel)
        await self.start_playback(ctx, player)

def setup(bot):
    bot.add_cog(Music(bot))
