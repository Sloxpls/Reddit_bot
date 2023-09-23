import os
import random
import json

from moviepy.audio.fx import audio_fadein, audio_fadeout
from moviepy.editor import VideoFileClip

from moviepy.editor import (
    concatenate_audioclips,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    VideoFileClip,
    AudioFileClip
)

class FinalVideo:
    def __init__(self, config, reddit_fetcher, tts, subclips):
        self.config = config
        self.reddit_fetcher = reddit_fetcher
        self.subclips = subclips
        self.total_length = subclips.total_length
        self.create_final_video()

    def create_final_video(self):
        save_path = self.create_save_path(None)
        background_video_path = self.background_selector()
        audio_clip_list = self.subclips.audio_clip_list
        text_clips_list = self.subclips.text_clips_list
        image_clip = VideoFileClip(background_video_path)
        background_audio_path = r"assets/backgrounds/audio/Mellow Vibes Radio-chill-summer.mp3"

        aspect_ratio = 9 / 16
        width = 1920
        height = 1080
        new_width = int(height * aspect_ratio)
        x1 = (width - new_width) / 2
        x2 = x1 + new_width
        y1 = 0
        y2 = height
        image_clip = image_clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

        if self.config.create_subclips and not self.config.create_full:
            finalvideo_list = self.split_into_subclips(audio_clip_list, text_clips_list, image_clip)
            self.export_subclips(finalvideo_list)
        else:
            self.export_full_video(audio_clip_list, text_clips_list, image_clip, save_path, background_audio_path)

        self.write_to_history()

    def background_selector(self):
        path_to_backgrounds = os.path.join(os.getcwd(), "assets", "backgrounds", "video")
        if self.config.background != "":
            background_file_path = os.path.join(path_to_backgrounds, self.config.background + ".mp4")
        else:
            file_list = os.listdir(path_to_backgrounds)
            background = random.choice(file_list)
            background_file_path = os.path.join(path_to_backgrounds, background)
        return background_file_path

    def split_into_subclips(self, audio_clip_list, text_clips_list, image_clip):
        finalvideo_list = []
        audio_temp = []
        text_temp = []
        duration_clip = 0
        total_duration = sum(audio.duration for audio in audio_clip_list)
        count2 = 0
        count = 1
        for audio_clip, text_clip in zip(audio_clip_list, text_clips_list):
            duration_clip += audio_clip.duration
            if duration_clip < self.config.length_of_subclip:
                audio_temp.append(audio_clip)
                text_temp.append(text_clip)
            else:
                audio = concatenate_audioclips(audio_temp)
                text = concatenate_videoclips(text_temp)
                background_clip = self.get_background_video(image_clip, audio)
                final_video_full = CompositeVideoClip([background_clip, text.set_position('center')])
                finalvideo_list.append(final_video_full)
                audio_temp = [audio_clip_list[0]]
                text_temp = [text_clips_list[0]]
                duration_clip = audio_clip_list[0].duration
                count += 1
                count2 += 1
        if len(audio_temp) != 0:
            audio = concatenate_audioclips(audio_temp)
            text = concatenate_videoclips(text_temp)
            background_clip = self.get_background_video(image_clip, audio)
            final_video_full = CompositeVideoClip([background_clip, text.set_position('center')])
            finalvideo_list.append(final_video_full)
        return finalvideo_list

    def create_save_path(self, count):
        save_path_file = f"{self.reddit_fetcher.title_text}"
        bad_char_list = [
            "/", "\\", ".", "@", "%", "*", ":", "<", ">", "\n", "?", "|", '"', "'", "`", "#", "{", "}",
            "[", "]", "(", ")", "&", "$", "!", "^", "~", "+", "=", ",", ";"
        ]
        for char in bad_char_list:
            save_path_file = save_path_file.replace(char, "")

        save_path_dir = os.path.join(os.getcwd(), "finishedVideo", self.reddit_fetcher.subreddit)
        if not os.path.exists(save_path_dir):
            os.makedirs(save_path_dir)

        if count is None:
            save_path = os.path.join(save_path_dir, save_path_file + ".WebM")
        else:
            save_path = os.path.join(save_path_dir, f"{count}-{save_path_file}.WebM")

        return save_path

    def write_to_history(self):
        video_history_path = os.path.join(os.getcwd(), "assets", "json", "history.json")
        with open(video_history_path, "r") as history_file:
            history_dict = json.load(history_file)

        history_dict[self.reddit_fetcher.post_id] = {
            "create_full": self.config.create_full,
            "create_subclips": self.config.create_subclips,
            "fps": self.config.fps,
            "length_of_subclip": self.config.length_of_subclip,
            "background": self.config.background,
            "voice": self.config.voice,
            "subreddit": self.config.subreddits,
        }

        with open(video_history_path, "w") as history_file:
            json_o = json.dumps(history_dict, indent=4)
            history_file.write(json_o)

    def get_background_video(self, image_clip, audio_clip_full):
        video_length = image_clip.duration

        random_time = random.randrange(180, int(video_length) - int(audio_clip_full.duration))
        end_time = random_time + audio_clip_full.duration

        image_clip = image_clip.subclip(random_time, end_time)

        background_minus_text = image_clip.set_audio(audio_clip_full)

        return background_minus_text

    def add_part_number(self, video, count, finalvideo_list, save_path_subclip):
        text = f"Part {count}/{len(finalvideo_list)}"
        add_text = TextClip(text, fontsize=80, bg_color='rgb(255,0,0)', color="rgb(255,255,255)").set_position(
            "center").set_duration(
            2)
        final = CompositeVideoClip([video, add_text])

        final.write_videofile(save_path_subclip, fps=self.config.fps, threads=os.cpu_count(), codec='libx264')

    def export_full_video(self, audio_clip_list, text_clips_list, image_clip, save_path, background_audio_path,
                          background_audio_volume=0.1):
        # Concatenate audio clips from the audio_clip_list
        audio_clip_full = concatenate_audioclips(audio_clip_list)

        # Concatenate video clips from the text_clips_list
        text_clip_full = concatenate_videoclips(text_clips_list)

        # Load the background audio
        background_audio_path = self.Get_background_audio_path()
        background_audio = AudioFileClip(background_audio_path)

        # Set the duration of the background audio to match the duration of text_clip_full
        background_audio = background_audio.set_duration(text_clip_full.duration)

        # Lower the volume of the background audio
        background_audio = background_audio.volumex(background_audio_volume)

        # Set the audio of text_clip_full to the background audio
        text_clip_full = text_clip_full.set_audio(background_audio)

        # Create the background video without text by combining image_clip and audio_clip_full
        background_minus_text = self.get_background_video(image_clip, audio_clip_full)

        # Create the final video by overlaying text_clip_full on top of background_minus_text
        final_video_full = CompositeVideoClip([background_minus_text, text_clip_full.set_position('center')])

        # Write the final video to the specified save_path
        final_video_full.write_videofile(
            save_path,
            fps=self.config.fps,
            threads=os.cpu_count(),
            codec='libvpx',
            preset='ultrafast',
            ffmpeg_params=['-b:v', '2M']
        )

    def export_subclips(self, finalvideo_list):
        for count, video in enumerate(finalvideo_list, start=1):
            save_path_subclip = self.create_save_path(count)
            self.add_part_number(video, count, finalvideo_list, save_path_subclip)


    def Get_background_audio_path(self):
        path_to_backgrounds_audio = os.path.join(os.getcwd(), "assets", "backgrounds", "audio")
        """
        if self.config.background != "":
            background_audio_path = os.path.join(path_to_backgrounds_audio, self.config.background + ".mp3")
        else:
            file_list = os.listdir(path_to_backgrounds_audio)
            background = random.choice(file_list)
            background_audio_path = os.path.join(path_to_backgrounds_audio, background)
        return background_audio_path
        """

        file_list = os.listdir(path_to_backgrounds_audio)
        background = random.choice(file_list)
        background_audio_path = os.path.join(path_to_backgrounds_audio, background)
        return background_audio_path

