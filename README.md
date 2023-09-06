Overview:
The Reddit Video Generator is a Python script designed to help you create engaging videos from Reddit posts. It automates the process of fetching top posts from specified subreddits, converting post text to speech, and combining it with background videos.
The script will fetch posts, generate videos, and save them in the specified output directory.
On the first run of the script, you will be askt to fill in all the config options, then it will automatically download background videos from YouTube for later use. This initial download ensures that you have a variety of backgrounds to work with.
Follow these steps to get started:

------------------------------------------------
Installation:
First, make sure you have Python 3.x installed on your system.

Install the required Python packages by running the following command in your terminal or command prompt:

Copy code
pip install -r requirements.txt |
python main.py

------------------------------------------------
Configuration:
You can customize its behavior by adjusting settings in the config.json file. Here's a breakdown of the key configuration options:

subreddits: Specify the list of subreddits to fetch posts from (e.g., "subreddits": "funny-pics-pics").

top_or_hot: Choose whether to fetch top or hot posts from the subreddits (e.g., "top_or_hot": "top").

post_preview: Toggle to show a preview of fetched posts (true/false).

create_full: Decide whether to create full-length videos (true/false).

create_subclips: Choose to create subclips if create_full is set to false (true/false).

fps: Set the frames per second for video output.

length_of_subclip: Define the maximum duration of subclips (in seconds).

background: Specify a background video (leave empty for random selection).

voice: Choose a voice for text-to-speech (1 for Australian male voice, 2 for Australian female voice, 3 for manual selection).

username, password, client_id, client_secret: Enter your Reddit API credentials (required for authentication).

video_download_dir: Directory to store downloaded background videos.

audio_download_dir: Directory to store downloaded background audio.
------------------------------------------------





