from typing import Union
from pathlib import Path
import requests
import tweepy
import jsonlines


class JsonlStreamListener(tweepy.StreamListener):
    def __init__(self, jsonl_path: Union[Path, str]) -> None:
        super().__init__()
        self.writer = jsonlines.Writer(open(jsonl_path, "w+"))

    def on_connect(self) -> None:
        print("Stream starts..")

    def on_closed(self, response: requests.Response) -> None:
        self.writer.close()

    def on_status(self, status: tweepy.Status) -> None:
        self.writer.write(status._json)

    def on_error(self, status_code: int) -> bool:
        print(f"Status code: {status_code}")
        return True

    def on_timeout(self) -> bool:
        return True
