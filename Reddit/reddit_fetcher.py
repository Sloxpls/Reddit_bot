import json
import os
import praw
from colorama import Fore

class RedditFetcher:
    def __init__(self, config, subreddit_count, reddit_post_id):
        self.reddit_post_id = reddit_post_id
        self.config = config
        self.subreddit_count = subreddit_count
        self.history_dict = self.load_history()
        self.with_post_id()
        self.random_voice()

    def fetch_top_post(self):
        all_subreddits = self.config.subreddits.split("-")

        if len(all_subreddits) < self.subreddit_count + 1:
            subreddit_to_use = all_subreddits[0]
        else:
            subreddit_to_use = all_subreddits[self.subreddit_count]

        subreddit = self.reddit.subreddit(subreddit_to_use)

        submissions = subreddit.top(limit=None) if self.config.top_or_hot == "top" else subreddit.hot(limit=None)

        for submission in submissions:
            submission_id = str(submission)

            if submission_id not in self.history_dict:
                if submission_id not in self.reddit_post_id:

                    if not self.config.post_preview:
                        self.submission = submission
                        return
                    else:
                        self.print_submission_info(submission)
                        if input(Fore.BLUE + "Do you want to create this video? [Y/N]: " + Fore.RESET).strip().upper() == "Y":
                            self.submission = submission
                            return

    def with_post_id(self):
        self.reddit = praw.Reddit(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            user_agent=self.config.user_agent,
            username=self.config.username,
            password=self.config.password
        )

        if self.config.post_id != "":
            post_id = self.config.post_id
            submission = self.reddit.submission(id=post_id)
            self.submission = submission
            self.create_text()
        else:
            self.fetch_top_post()
            self.create_text()


    def load_history(self):
        history_file_path = os.path.join(os.getcwd(), "assets", "json", "history.json")

        if os.path.exists(history_file_path):
            try:
                with open(history_file_path, "r") as history_file:
                    return json.load(history_file)
            except json.JSONDecodeError:
                pass
        else:
            # Create an empty history file if it doesn't exist
            with open(history_file_path, "w") as history_file:
                json.dump({}, history_file)

        return {}

    def save_history(self):
        history_file_path = os.path.join(os.getcwd(), "assets", "json", "history.json")

        with open(history_file_path, "w") as history_file:
            json.dump(self.history_dict, history_file, indent=4)

    def print_submission_info(self, submission, is_new=False):
        # Define colors for separator
        separator_color = Fore.YELLOW

        # Print the submission information with formatting
        separator = separator_color + "---------------------------------------------------" + separator_color
        print(separator)
        print(f"Scraping {submission.subreddit}\n{submission.title}")
        print(f"{submission.url}")
        print(separator)

    def create_text(self):
        url = self.submission.url
        post_id = self.submission.id
        title_text = self.submission.title
        self_text = self.submission.selftext if self.submission.selftext else ""

        # Store the retrieved information as instance variables
        self.url = url
        self.post_id = post_id
        self.title_text = title_text
        self.self_text = self_text
        self.subreddit = self.submission.subreddit.display_name

        # Print a clear message indicating that text has been read and stored
        separator = "---------------------------------------------------"
        print(Fore.GREEN + f"\n{separator}" + Fore.RESET)  # Green text for separator line
        print(Fore.GREEN + "Text read and stored successfully!" + Fore.RESET)  # Green text for success message
        print(Fore.GREEN + separator + "\n" + Fore.RESET)  # Green text for separator line

    def random_voice(self):
        voice_int = self.config.voice

        if voice_int == 1:
            self.voice = "en_au_001"
        elif voice_int == 2:
            self.voice = "en_au_002"
        elif voice_int == 3:
            choice = input(Fore.BLUE + "Male or female voice [M/F]: " + Fore.RESET).lower()  # Blue text for input
            self.voice = "en_au_002" if choice == "m" else "en_au_001"
