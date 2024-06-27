import os
import discord
from pytube import YouTube
from pytube.exceptions import RegexMatchError

async def convert_video_to_mp3(ctx, url):
    try:
        yt = YouTube(url)

        if not yt.streams.filter(only_audio=True).first():
            await ctx.send("Error: This video does not contain audio.")
            return

        video_title = yt.title

        download_dir = '/discordbot/bot/temp'
        output_dir = '/discordbot/bot/output'

        temp_audio_path = os.path.join(download_dir, 'temp_audio.mp3')
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=download_dir, filename='temp_audio.mp3')

        output_audio_path = os.path.join(output_dir, f'{video_title}.mp3')
        os.rename(temp_audio_path, output_audio_path)

        await ctx.send(file=discord.File(output_audio_path))

        os.remove(output_audio_path)

        print('Conversion completed successfully!')

    except RegexMatchError:
        await ctx.send("Error: Invalid YouTube URL. Please provide a valid video URL.")
    except Exception as e:
        print(f'Error during conversion: {e}')
        await ctx.send('Error during conversion. Please try again.')


