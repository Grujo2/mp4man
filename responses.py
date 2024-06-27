import os
import discord
from pytube import YouTube
from pytube.exceptions import RegexMatchError


async def convert_video(ctx, url, format_choice):
    try:
        yt = YouTube(url)

        download_dir = '/discordbot/bot/temp'
        output_dir = '/discordbot/bot/output'

        os.makedirs(download_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        if format_choice == 'mp3':
            if not yt.streams.filter(only_audio=True).first():
                await ctx.send("Error: This video does not contain audio.")
                return

            temp_audio_path = os.path.join(download_dir, 'temp_audio.mp3')
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(output_path=download_dir, filename='temp_audio.mp3')

            output_audio_path = os.path.join(output_dir, f'{yt.title}.mp3')
            os.rename(temp_audio_path, output_audio_path)

            await ctx.send(f"Conversion to MP3 completed. Attaching MP3 file...")
            await ctx.send(file=discord.File(output_audio_path))
            os.remove(output_audio_path)
            print('Conversion to MP3 completed successfully!')

        elif format_choice == 'mp4':
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            download_dir = '/discordbot/bot/temp'

            video_file = video_stream.download(output_path=download_dir)

            mp4_file = os.path.join(output_dir, f'{yt.title}.mp4')
            if os.path.exists(mp4_file):
                mp4_file = os.path.join(output_dir, f'{yt.title}_{yt.streams.first().itag}.mp4')

            os.rename(video_file, mp4_file)
            await ctx.send(f"Conversion to MP4 completed. Attaching MP4 file...")
            await ctx.send(file=discord.File(mp4_file))

            os.remove(mp4_file)
            print('Conversion to MP4 completed and file sent!')

        else:
            await ctx.send("Error: Invalid format choice. Use '?c <url> <mp3/mp4>'")

    except RegexMatchError:
        await ctx.send("Error: Invalid YouTube URL. Please provide a valid video URL.")
    except FileExistsError as e:
        await ctx.send(f"Error: File already exists. {e}")
    except Exception as e:
        print(f'Error during conversion: {e}')
        await ctx.send(f'Error during conversion: {e}. Please try again.')
