import tweepy
import sys
import json
import time as time

print("Remember to adjust your twitter access tokens to download the tweets")

consumer_key = 'REPLACE ME'
consumer_key_secret = 'REPLACE ME'
access_token = 'REPLACE ME'
access_token_secret = 'REPLACE ME'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweet_id_file = "./tweet_ids.txt"
output_filename_json = "./tweets_fetched.jsonlines"
output_broken_twweets = "./broke_tweets_ids.json"
sleepTime = 2

broken_ids = {"ids":None}
ids = []
with open(tweet_id_file) as input_file:
    for example_num, id_per_line in enumerate(input_file.read().splitlines()):
        tweet = {"tweet_id": id_per_line}
        print(f"Try to fetch tweet id : {id_per_line}")
        with open(output_filename_json, 'a', encoding="utf8") as output_file:
            try:
                tweetFetched = api.get_status(tweet["tweet_id"])
                tweet["author_id"] = tweetFetched.author.id_str
                tweet["author_name"] = tweetFetched.author.name
                tweet["text"] = tweetFetched.text
                print("Tweet fetched" + tweet["text"])
                output_file.write(json.dumps(tweet))
                output_file.write("\n")
                #To avoid being kicked out downloading to aggressively...
                time.sleep(sleepTime)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                print(f"tweet id :{tweet['tweet_id']} does probably not exist anymore")
                ids.append(id_per_line)
                continue
        print(f"Fetched tweet id : {id_per_line}")

if len(ids) > 0:
    broken_ids["ids"]=ids
    print("These twitter ids are no longer available.")
    print(broken_ids)

    with open(output_broken_twweets, 'a', encoding="utf8") as output_file:
        output_file.write(json.dumps(broken_ids))
        output_file.write("\n")
