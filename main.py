from typing import Union
from pathlib import Path
import tweepy
from listener import JsonlStreamListener
from utils import read_json


def listen_bist_tickers_stream(
    tw_api_creds_path: Union[Path, str],
    bist_tickers_path: Union[Path, str],
    output_jsonl_path: Union[Path, str],
    bist_index: str = "xu030",
    add_number_sign: bool = True,
    only_tr_tweets: bool = True,
) -> None:
    creds = read_json(tw_api_creds_path)
    bist_tickers = read_json(bist_tickers_path)

    assert bist_index in bist_tickers.keys(), f"Unknown index, expected: {bist_tickers.keys()}"

    auth = tweepy.OAuthHandler(consumer_key=creds["consumer_token"], consumer_secret=creds["consumer_secret"])
    auth.set_access_token(key=creds["access_token"], secret=creds["access_token_secret"])

    listener = JsonlStreamListener(jsonl_path=output_jsonl_path)
    stream = tweepy.Stream(auth=auth, listener=listener)

    track = [f"#{t}" if add_number_sign else t for t in bist_tickers[bist_index]]
    languages = ["tr"] if only_tr_tweets else None

    stream.filter(track=track, languages=languages)


if __name__ == "__main__":
    tw_api_creds_path = "tw_api_creds.json"
    bist_tickers_path = "data/bist_tickers_list.json"
    output_jsonl_path = "bist_tickers_tweets.jsonl"
    listen_bist_tickers_stream(tw_api_creds_path, bist_tickers_path, output_jsonl_path)