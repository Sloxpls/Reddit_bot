import os
import textwrap
from moviepy.editor import AudioFileClip, TextClip

class VideoCreator:
    def __init__(self, config, reddit_fetcher, tts):
        self.audio_clip_list = None
        self.text_clips_list = None
        self.total_length = None
        self.config = config
        self.reddit_fetcher = reddit_fetcher
        self.tts = tts
        self.file_path_to_mp3 = f"{config.subreddits}-{reddit_fetcher.post_id}"
        self.file_path_to_temp = os.path.join(os.getcwd(), "assets", "temp", "mp3", reddit_fetcher.post_id)
        self.output_file_dir = os.path.join(os.getcwd(), "finishedVideo", config.subreddits)

        self.calculate_total_length_of_mp3_files()
        self.create_full()

    def calculate_total_length_of_mp3_files(self):
        directory_path = os.path.join(os.getcwd(), "assets", "temp", "mp3", self.reddit_fetcher.post_id)

        total_length = 0
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            for filename in os.listdir(directory_path):
                if filename.endswith(".mp3"):
                    file_path = os.path.join(directory_path, filename)
                    audio_clip = AudioFileClip(file_path)
                    total_length += audio_clip.duration
        self.total_length = total_length

    def create_full(self):
        audio_clip_list = []
        text_clips_list = []

        clip_title = os.path.join(
            os.getcwd(),
            "assets",
            "temp",
            "mp3",
            self.reddit_fetcher.post_id,
            f"{self.config.subreddits}-{self.reddit_fetcher.post_id}-0.mp3"
        )
        audio_clip = AudioFileClip(clip_title)
        audio_clip_duration = audio_clip.duration
        txt_clip = self.get_clip_text(None, audio_clip_duration)
        text_clips_list.append(txt_clip)
        audio_clip_list.append(audio_clip)

        for x in range(len(self.tts.chunks)):
            clip = os.path.join(
                os.getcwd(),
                "assets",
                "temp",
                "mp3",
                self.reddit_fetcher.post_id,
                f"{self.config.subreddits}-{self.reddit_fetcher.post_id}-{x + 1}.mp3"
            )
            audio_clip = AudioFileClip(clip)
            audio_clip_duration = audio_clip.duration
            txt_clip = self.get_clip_text(x, audio_clip_duration)

            text_clips_list.append(txt_clip)
            audio_clip_list.append(audio_clip)

            self.text_clips_list = text_clips_list
            self.audio_clip_list = audio_clip_list

    def get_clip_text(self, count, audio_clip_duration):
        text = []

        if count is None:
            lines = textwrap.wrap(self.reddit_fetcher.title_text, width=55)
        else:
            lines = textwrap.wrap(self.tts.chunks[count], width=55)

        for line in range(len(lines)):
            text.append(lines[line])
            text.append('\n')
        text = ''.join(text)
        txt_clip = TextClip(
            text,
            fontsize=40,
            color='rgb(255,255,255)',
            bg_color="rgba(48, 48, 48, 0.9)",
            size=(1000, 500),
            method='caption'
        )

        txt_clip = txt_clip.set_duration(audio_clip_duration + 0.5).set_position('center')

        return txt_clip
