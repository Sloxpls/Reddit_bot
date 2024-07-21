import os

from TextToSpeech.local_tts import local_TTS


class TextProcessor:
    def __init__(self, config, reddit_fetcher):
        self.voice = reddit_fetcher.voice
        self.file_dir = None
        self.config = config
        self.post_id = reddit_fetcher.post_id
        self.chunks = None
        self.title_text = reddit_fetcher.title_text
        self.self_text = reddit_fetcher.self_text
        self.split_text_into_chunks()
        self.create_dir_for_mp3()
        self.create_mp3_files()

    def split_text_into_chunks(self, max_chunk_length=200):
        chunks = []
        words = self.self_text.split()
        current_chunk = ""

        for word in words:
            if len(current_chunk) + len(word) + 1 <= max_chunk_length:
                if current_chunk:
                    current_chunk += " "
                current_chunk += word
            else:
                chunks.append(current_chunk)
                current_chunk = word

        if current_chunk:
            chunks.append(current_chunk)

        self.chunks = chunks

    def create_dir_for_mp3(self):
        file_dir = os.path.join(os.getcwd(), "assets", "temp", "mp3", self.post_id)
        self.file_dir = file_dir
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

    def create_mp3_files(self):
        file_name = f"{self.config.subreddits}-{self.post_id}-0.mp3"
        file_name = os.path.join(self.file_dir, file_name)

        # Print a yellow separator
        separator_yellow = "\033[93m" + "--------------------------------" + "\033[0m"
        print(separator_yellow)

        # Print a message in yellow
        print("\033[93m" + f"Creating sound for {self.title_text}" + "\033[0m")

        tts = local_TTS()
        tts.run(self.title_text, file_name)
        count = 1

        for text in self.chunks:
            file_name = f"{self.config.subreddits}-{self.post_id}-{count}.mp3"
            file_name = os.path.join(self.file_dir, file_name)
            tts.run(text, file_name)
            count += 1

        # Print "Done!!" in green
        separator_green = "\033[92m" + "Done!!" + "\033[0m"
        print(separator_green)
