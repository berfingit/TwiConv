import json
from nltk.tokenize import WhitespaceTokenizer

import os


#file produced by fetch_tweets.py
tweets = "./tweets_fetched.jsonlines"
author_directory = "./author"
tweet_text_directory = "./text"

# The withespace Tokenizer might not be sufficient, to handle the tokenizing. Not sure how it behaves with
# the nospace unicode character.
tk = WhitespaceTokenizer()


with open(tweets) as input_file:
    for example_num, line in enumerate(input_file.read().splitlines()):
        #tweet_id, autor_id, author_name, text
        json_tweet = json.loads(line)
        text_file_name = f"{json_tweet['tweet_id']}.txt"
        tokenized_text = tk.tokenize(json_tweet["text"])
        author = json_tweet["author_name"]
        author_file = os.path.join(author_directory, text_file_name)
        text_file = os.path.join(tweet_text_directory, text_file_name)
        with open(author_file, 'a', encoding="utf8") as output_file:
            output_file.write(author)
            output_file.write("\n")
        with open(text_file, 'a', encoding="utf8") as output_file:
            for token in tokenized_text:
                output_file.write(token)
                output_file.write("\n")
