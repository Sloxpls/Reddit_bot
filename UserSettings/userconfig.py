import json
import os
from typing import Optional

class ConfigManager:
    sessionid = ""

    def __init__(self) -> None:
        self.json_conf_path = "assets/json/config.json"
        self.print_caution_message()
        self.load_existing_config()
        self.prompt_missing_values()
        self.save_to_json()
        self.create_tiktok_sessionid()

    def load_existing_config(self) -> None:
        try:
            if os.path.exists(self.json_conf_path):
                with open(self.json_conf_path, "r") as config_file:
                    config_data = json.load(config_file)

                # Assign existing values to class variables
                self.client_id: Optional[str] = config_data.get("client_id", None)
                self.client_secret: Optional[str] = config_data.get("client_secret", None)
                self.user_agent: Optional[str] = config_data.get("user_agent", None)
                self.username: Optional[str] = config_data.get("username", None)
                self.password: Optional[str] = config_data.get("password", None)
                self.create_full: Optional[bool] = config_data.get("create_full", None)
                self.create_subclips: Optional[bool] = config_data.get("create_subclips", None)
                self.fps: int = config_data.get("fps", 30)
                self.length_of_subclip: Optional[int] = config_data.get("length_of_subclip", None)
                self.background: str = config_data.get("background", "")
                self.post_preview: Optional[bool] = config_data.get("post_preview", None)
                self.amount_of_post: Optional[int] = config_data.get("amount_of_post", None)
                self.voice: int = config_data.get("voice", 3)
                self.subreddits: Optional[str] = config_data.get("subreddits", None)
                self.post_id: Optional[str] = config_data.get("post_id", None)
                self.top_or_hot: str = config_data.get("top_or_hot", "hot")
                self.tiktok_sessionid: Optional[str] = config_data.get("tiktok_sessionid", None)
            else:
                self.client_id = None
                self.client_secret = None
                self.user_agent = None
                self.username = None
                self.password = None
                self.create_full = None
                self.create_subclips = None
                self.fps = 30
                self.length_of_subclip = None
                self.background = "Minecraft.mp4"
                self.post_preview = None
                self.amount_of_post = None
                self.voice = 3
                self.subreddits = None
                self.post_id = None
                self.top_or_hot = "hot"
                self.tiktok_sessionid = None

        except Exception as e:
            print("Error loading existing configuration:", e)

    def prompt_missing_values(self) -> None:
        try:
            if self.client_id is None:
                self.client_id = input("Client ID: ")

            if self.client_secret is None:
                self.client_secret = input("Client Secret: ")

            if self.user_agent is None:
                self.user_agent = input("User Agent: ")

            if self.username is None:
                self.username = input("Username: ")

            if self.password is None:
                self.password = input("Password: ")

            if self.tiktok_sessionid is None:
                self.tiktok_sessionid = input("TikTok SessionId: ")

            if self.create_full is None:
                self.create_full = input("Create full clips? (True/False): ").strip().lower() == "true"

            if self.create_subclips is None:
                self.create_subclips = input("Create subclips? (True/False): ").strip().lower() == "true"

            if self.fps is None:
                self.fps = int(input("FPS (frames per second): "))

            if self.length_of_subclip is None:
                self.length_of_subclip = int(input("Length of subclip (in seconds): "))

            if self.background is None:
                self.background = input("Background video file: ")

            if self.post_preview is None:
                self.post_preview = input("Post preview? (True/False): ").strip().lower() == "true"

            if self.amount_of_post is None:
                self.amount_of_post = int(input("Amount of posts: "))

            if self.voice is None:
                self.voice = int(input("Voice number: "))

            if self.subreddits is None:
                self.subreddits = input("Subreddits (comma-separated): ")

            if self.post_id is None:
                self.post_id = input("Post ID: ")

            if self.top_or_hot is None:
                self.top_or_hot = input("Top or Hot? (top/hot): ").strip().lower()

        except Exception as e:
            print("Error prompting for missing values:", e)

    def save_to_json(self) -> None:
        try:
            config_data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "user_agent": self.user_agent,
                "username": self.username,
                "password": self.password,
                "create_full": self.create_full,
                "create_subclips": self.create_subclips,
                "fps": self.fps,
                "length_of_subclip": self.length_of_subclip,
                "background": self.background,
                "post_preview": self.post_preview,
                "amount_of_post": self.amount_of_post,
                "voice": self.voice,
                "subreddits": self.subreddits,
                "post_id": self.post_id,
                "top_or_hot": self.top_or_hot,
                "tiktok_sessionid": self.tiktok_sessionid
            }

            with open(self.json_conf_path, "w") as config_file:
                json.dump(config_data, config_file, indent=4)

        except Exception as e:
            print("Error saving configuration to JSON:", e)

    def print_caution_message(self):
        creator_prompt = """
        ****************************************************
        **                                                **
        **   This program was created by Sloxpls.         **
        **                                                **
        ****************************************************
        """
        print("\033[92m" + creator_prompt + "\033[0m")  # Green text for creator prompt

        warning_message = """
        ****************************************************
        **                                                **
        **   CAUTION: Please be careful when entering     **
        **   configuration values. Ensure they are of     **
        **   the correct type and format. Some settings   **
        **   may overwrite others. If the program crashes,**
        **   consider removing the config JSON file and   **
        **   trying again.                                **
        **                                                **
        **   Enjoy using the program!                     **
        **                                                **
        ****************************************************
        """
        print("\033[91m" + warning_message + "\033[0m")  # Red text for warning message

    def create_tiktok_sessionid(self):
        ConfigManager.sessionid = self.tiktok_sessionid
