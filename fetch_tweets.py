# import tweepy
import sys
import json
import time as time
import argparse
import stweet as st
from stweet.tweets_by_ids_runner.tweets_by_id_context import TweetsByIdContext
from stweet.model import UserTweetRaw
import json



class SingleTweetContext(TweetsByIdContext):
    def __setattr__(self, __name: str, __value: any) -> None:
        if __name == "cursor":
            __value = None
        return super().__setattr__(__name, __value)
    


def to_json(raw_tweet: UserTweetRaw):
    return {
        "object_type": raw_tweet.object_type,
        "download_datetime": raw_tweet.download_datetime.isoformat(),
        "raw_value": json.loads(raw_tweet.raw_value),
    }


def process_raw_tweets(tweet_id: str, raw_list: list[UserTweetRaw]) -> dict:

    for raw_tweet in raw_list:
        tweet = to_json(raw_tweet)
        if tweet["raw_value"]["rest_id"] == tweet_id:
            return tweet

    print(f"Tweet {tweet_id} not found!")
    return None


tweet_id_file = "./tweet_ids.txt"
output_filename_json = "./tweets_fetched.jsonlines"
output_broken_tweets = "./broken_tweet_ids.txt"
sleepTime = 2

def try_tweet_by_id_scrap(id: str, single_tweet: bool = True):
    id_task = st.TweetsByIdTask(id)
    output_json = st.JsonLineFileRawOutput(f"data/tweets/{id}.jl")
    output_print = st.PrintRawOutput()
    output_tweets = st.CollectorRawOutput()

    st.TweetsByIdRunner(
        tweets_by_id_task=id_task,
        raw_data_outputs=[output_tweets],
        tweets_by_ids_context=SingleTweetContext() if single_tweet else None,
    ).run()

    raw_list = output_tweets.get_raw_list()

    tweet = process_raw_tweets(id, raw_list)

    #raise error if tweet is not found
    if tweet is None:
        raise Exception("Tweet not found")
    
    return tweet


broken_ids = []
with open(tweet_id_file) as input_file:
    for i, id_per_line in enumerate(input_file.read().splitlines()):
        tweet = {"tweet_id": id_per_line}
        print(f"Try to fetch tweet id : {id_per_line}")
        with open(output_filename_json, 'a', encoding="utf8") as output_file:
            try:
                tweet_scrap = try_tweet_by_id_scrap(tweet["tweet_id"], True)    
                tweet["author_id"] = tweet_scrap["raw_value"]["core"]["user_results"]["result"]["rest_id"]
                tweet["author_name"] = tweet_scrap["raw_value"]["core"]["user_results"]["result"]["legacy"]["screen_name"]
                tweet["text"] = tweet_scrap["raw_value"]["legacy"]["full_text"]
                print("Tweet fetched" + tweet["text"])
                output_file.write(json.dumps(tweet))
                output_file.write("\n")
                #To avoid being kicked out downloading to aggressively...
                time.sleep(sleepTime)
            except Exception as e:
                print("Unexpected error:", e)
                # print("Unexpected error:", sys.exc_info()[0])
                print(f"tweet id :{tweet['tweet_id']} does probably not exist anymore")
                broken_ids.append(id_per_line)
                continue
        print(f"Fetched tweet id : {id_per_line}")

if broken_ids:
    print(f"{len(broken_ids)} tweets are no longer available.")
    print(f"Saving broken ids in {output_broken_tweets}")


    with open(output_broken_tweets, 'a', encoding="utf8") as output_file:
        for id in broken_ids:
            output_file.write(id)
            output_file.write("\n")

