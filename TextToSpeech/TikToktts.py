# documentation for tiktok api: https://github.com/oscie57/tiktok-voice/wiki
import base64
import random
import time
from typing import Optional, Final

import requests
from UserSettings.userconfig import ConfigManager

__all__ = ["TikTok", "TikTokTTSException"]

class TikTok:
    """TikTok Text-to-Speech Wrapper"""

    def __init__(self):
        headers = {
            "User-Agent": "com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; "
            "Build/NRD90M;tt-ok/3.12.13.1)",
            "Cookie": f"sessionid={ConfigManager.sessionid}",
        }

        self.URI_BASE = "https://api16-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/"
        self.max_chars = 200

        self._session = requests.Session()
        # set the headers to the session, so we don't have to do it for every request
        self._session.headers = headers

    def run(self, text: str, filepath: str, voice: str ):


        # get the audio from the TikTok API
        data = self.get_voices(voice=voice, text=text)

        # check if there was an error in the request
        status_code = data["status_code"]
        if status_code != 0:
            raise TikTokTTSException(status_code, data["message"])

        # decode data from base64 to binary
        try:
            raw_voices = data["data"]["v_str"]
        except:
            print(
                "The TikTok TTS returned an invalid response. Please try again later, and report this bug."
            )
            raise TikTokTTSException(0, "Invalid response")
        decoded_voices = base64.b64decode(raw_voices)

        # write voices to specified filepath
        with open(filepath, "wb") as out:
            out.write(decoded_voices)

    def get_voices(self, text: str, voice: Optional[str] = None) -> dict:
        """If voice is not passed, the API will try to use the most fitting voice"""
        # sanitize text
        text = text.replace("+", "plus").replace("&", "and").replace("r/", "")

        # prepare url request
        params = {"req_text": text, "speaker_map_type": 0, "aid": 1233}

        if voice is not None:
            params["text_speaker"] = voice

        # send request
        try:
            response = self._session.post(self.URI_BASE, params=params)
        except ConnectionError:
            time.sleep(random.randrange(1, 7))
            response = self._session.post(self.URI_BASE, params=params)

        return response.json()



class TikTokTTSException(Exception):
    def __init__(self, code: int, message: str):
        self._code = code
        self._message = message

    def __str__(self) -> str:
        if self._code == 1:
            return f"Code: {self._code}, reason: probably the aid value isn't correct, message: {self._message}"

        if self._code == 2:
            return f"Code: {self._code}, reason: the text is too long, message: {self._message}"

        if self._code == 4:
            return f"Code: {self._code}, reason: the speaker doesn't exist, message: {self._message}"

        return f"Code: {self._message}, reason: unknown, message: {self._message}"