import json
import os
from pathlib import Path
import yt_dlp

class BackgroundDownloader:
    def __init__(self):
        self.video_download_dir = "./assets/backgrounds/video/"
        self.audio_download_dir = "./assets/backgrounds/audio/"
        self.download_background_video()
        self.download_background_audio()

    def download_background_video(self):
        background_videos = "assets/json/background_videos.json"
        with open(background_videos, "r") as json_file:
            data_dict = json.load(json_file)

            for key in data_dict:
                uri = data_dict[key][0]
                filename = data_dict[key][1]
                credit = data_dict[key][2]

                video_filepath = os.path.join(self.video_download_dir, f"{credit}-{filename}")

                if Path(video_filepath).is_file():
                    return

                self.download_background_data_message()

                print("Downloading background video...")
                ydl_opts = {
                    "format": "bestvideo[height<=1080][ext=mp4]",
                    "outtmpl": video_filepath,
                    "retries": 10,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([uri])

                print("Background video downloaded successfully!")

    def download_background_audio(self):
        background_audios = "assets/json/background_audios.json"
        with open(background_audios, "r") as json_file:
            data_dict = json.load(json_file)

            for key in data_dict:
                uri = data_dict[key][0]
                filename = data_dict[key][1]
                credit = data_dict[key][2]

                audio_filepath = os.path.join(self.audio_download_dir, f"{credit}-{filename}")

                if Path(audio_filepath).is_file():
                    return

                print("Downloading background audio...")
                ydl_opts = {
                    "outtmpl": audio_filepath,
                    "format": "bestaudio/best",
                    "extract_audio": True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([uri])

                print("Background audio downloaded successfully!")

    def download_background_data_message(self):
        print("\nPreparing to download background videos and audio from YouTube.")
        print("This action may take a while and is only needed once.")
        print("Please be patient while the downloads are in progress.\n")
