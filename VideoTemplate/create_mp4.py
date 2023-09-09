import os
import textwrap
import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import TextClip
from moviepy.video.compositing.concatenate import concatenate_videoclips


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

    from moviepy.editor import TextClip, concatenate_videoclips
    import textwrap

    def get_clip_text(self, count, audio_clip_duration):
        # Get the text to display based on the 'count' parameter
        if count is None:
            text = self.reddit_fetcher.title_text
        else:
            text = self.tts.chunks[count]


        # Calculate the duration for each word
        words = text.split()
        word_duration = (audio_clip_duration / len(words)) * 2

        two_word_list = []

        for i in range(0, len(words), 2):
            if i + 1 < len(words):
                two_word_list.append(words[i] + " " + words[i + 1])

        # Initialize a list to store subclips for each word
        subclips = []

        # Specify the path to your custom font file
        custom_font = r"C:\Users\jim\Desktop\Reddit_botV3\assets\fonts\Aloevera-OVoWO.ttf"  # Replace with the actual path

        # Create subclips for each word and apply crossfadein effect
        for word in two_word_list:
            word_clip = TextClip(word, fontsize=60, color='white', bg_color="rgba(48, 48, 48, 0.9)",
                                 size=(450, 200), method='caption', font=custom_font)
            word_clip = word_clip.set_duration(word_duration).crossfadein(0)
            subclips.append(word_clip)

        # Concatenate the subclips to create the final text clip
        txt_clip = concatenate_videoclips(subclips, method="compose")
        txt_clip = txt_clip.set_position('center')

        return txt_clip

