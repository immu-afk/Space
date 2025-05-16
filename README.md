# Discord Music Bot

A simple music bot for Discord using discord.py and Wavelink.

## Setup

1. Clone the repo or upload it directly to GitHub.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `config.json` file and add your bot token and prefix.
4. Run a Lavalink server (instructions below).
5. Run the bot:
   ```
   python bot.py
   ```

## Lavalink Setup

Download Lavalink from https://github.com/freyacodes/Lavalink/releases  
Create `application.yml` with:

```yaml
server:
  port: 2333
lavalink:
  server:
    password: youshallnotpass
    sources:
      youtube: true
      soundcloud: true
      spotify:
        clientId: YOUR_SPOTIFY_CLIENT_ID
        clientSecret: YOUR_SPOTIFY_CLIENT_SECRET
```

Run Lavalink with:

```
java -jar Lavalink.jar
```

---

## Commands

- `!join` - Bot joins your voice channel
- `!play <song name or url>` - Play a song or add to queue
- `!pause` - Pause playback
- `!resume` - Resume playback
- `!skip` - Skip current song
- `!stop` - Stop and clear queue
