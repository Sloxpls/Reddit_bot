from UserSettings.fileTree import dir_exist
from UserSettings.userconfig import ConfigManager
from Reddit.reddit_fetcher import RedditFetcher
from TextToSpeech.tts import TextProcessor
from VideoTemplate.create_mp4 import VideoCreator
from VideoTemplate.finalVideo import FinalVideo
from downlowds.bakgrunds import BackgroundDownloader
from cleaning.clean import remove_subdirectories


def main():
    dir_exist()
    config = ConfigManager()
    BackgroundDownloader()

    reddit_fetcher_list = []
    reddit_post_id = []

    # Fetch Reddit posts
    for subbredit_count in range(config.amount_of_post):
        reddit_fetcher = RedditFetcher(config, subbredit_count, reddit_post_id)
        reddit_post_id.append(reddit_fetcher.post_id)
        reddit_fetcher_list.append(reddit_fetcher)

    # Process text, create subclips, and generate final video
    for x in range(config.amount_of_post):
        tts = TextProcessor(config, reddit_fetcher_list[x])
        subclips = VideoCreator(config, reddit_fetcher_list[x], tts)
        FinalVideo(config, reddit_fetcher_list[x], tts, subclips)

    # Clean up temporary directories
    remove_subdirectories()


if __name__ == "__main__":
    main()
