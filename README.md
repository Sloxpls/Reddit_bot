## Overview
The Reddit Video Generator is a Python script designed to help you create engaging videos from Reddit posts. It automates the process of fetching top posts from specified subreddits, converting post text to speech, and combining it with background videos. The script will fetch posts, generate videos, and save them in the specified output directory. On the first run of the script, you will be asked to fill in all the config options, then it will automatically download background videos from YouTube for later use. This initial download ensures that you have a variety of backgrounds to work with.

Follow these steps to get started:

---

## Installation
First, make sure you have Python 3.x installed on your system.

Before you can use this Python script, you'll need to have ImageMagick installed on your system. ImageMagick is a powerful open-source software suite for displaying, converting, and editing images. You can download and install ImageMagick from their official website at [https://imagemagick.org/](https://imagemagick.org/).

Please make sure that ImageMagick is properly configured and accessible from the command line before running this script. Once ImageMagick is installed, you should be all set to use our Python script to perform various image-related tasks.
When installing ImageMagick you need to check the box legay utills
Install the required Python packages by running the following command in your terminal or command prompt:

```sh
pip install -r requirements.txt
```
```sh
pip install --upgrade setuptools
```
```sh
python main.py
```

## Configuration options
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


---

## TTS options
TTS and TikTok API Integration
The script supports both local TTS and TikTok API for generating speech. By default, the local TTS is used.

Local TTS
The local TTS engine converts text from Reddit posts to speech on your local machine. You don't need to do any additional setup beyond the initial installation of the required Python packages.

TikTok API
If you prefer to use TikTok's TTS service, you need to configure the TikTok API settings in the config.json file. Ensure you have the API credentials and set the use_tiktok_tts option to true. The TikTok API can offer different voice options and better quality. cod changes might be required


