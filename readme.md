alternative script for recreating [TwiConv](https://github.com/berfingit/TwiConv) dataset without a twitter access token.
powered by [stweet](https://github.com/markowanga/stweet)

## TwiConv Corpus

This is an instruction on how to reproduce the TwiConv Corpus as described in _TwiConv: A Coreference-annotated Corpus of Twitter Conversations_. TwiConv is an annotated corpus for nominal coreference in Twitter conversations (Twitter threads). To conform with Twitter's Developer Policy, we only share our annotations as text files without including the full tweet contents and authors. Instead we provide the tweet IDs and also share an additional script and data to map our tokenization and annotations to the original tweets.

### Required Data
- CoNLL skeleton files in which the words and tweet authors are anonymized (one file for each conversation/thread, provided in ``conll_skeleton``)
- files with token differences to re-create the tokenization (one file per tweet, provided in ``diff``)
- text files containing the message of each tweet. The tweets can be downloaded via their tweet ID through the Twitter API (all IDs are listed in ``tweet_ids.txt``).
- text files containing the author of each tweet (this is just one word per file, the username). The author can also be downloaded via the tweet ID.

### Make CoNLL-format files

After downloading all the tweets and authors via their Tweet IDs, the text of each tweet should be saved in an individual text file, with the tweet ID as the name and the .txt extension (e.g. ``0123456789.txt``). In a different directory, the authors should be stored in the same way, using the same file name (in this case ``0123456789.txt`` as well).

 Example tweet: ``This is just a test. Hi Twitter!``

The text then has to be tokenized on spaces (only spaces, not on punctuation etc.), with one token per line. A file should look like this:

 ```
 This
 is
 just
 a
 test.
 Hi
 Twitter!
 ```

If a tweet is no longer available, no files should be created (not even empty ones); the words and author will stay anonymized for this tweet.

**Note:** Some tweets may contain unusual characters like zero-width spaces, which make the spacing invisible. At those spaces, words should separated just like at visible spaces.
Specifically, in the tweet with ID ``950216535125082112``, the tokenized version of ``*** I can'tJks ***`` should be

```
***
I
can't
Jks
****
```

As a final step, running ``python make_conll.py <PATH TO TWEET TEXT FILES> <PATH TO AUTHOR FILES>`` will create the CoNLL files in ``conll``.

### Download the Tweets

You need to enter your generated Twitter access tokens for developer in fetch_tweets.py
Run this script and then run tokenize_tweets.py to prepare the data for the CoNLL processing.
The data is split in 2 directories namely, /author and /text .
### The CoNLL format

The CoNLL format is inspired by the original CoNLL-2012 format with some additional annotations.
Empty lines indicate sentence breaks.

```
COLUMN 		CONTENT
0 		Thread ID
1 		Thread number
2 		Token number in sentence
3 		Token
4 		POS tag
5 		Parse info
6 		Speaker/User handle
7 		Representative mention
8 		Semantic class
9 		NP form/reference type
10		Coreference ID
11		Clause boundary
12		Lowest-level NP boundary
13		Highest-level NP boundary
14		Grammatical role
15		Genericity
16		[Tweet number in thread]_[sentence number in tweet]_[token number in sentence]
```

### Citation

Berfin Aktaş and Annalena Kohnert. TwiConv: A Coreference-annotated Corpus of Twitter Conversations. In Proceedings of the Third Workshop on Computational Models of Reference, Anaphora and Coreference (CRAC@COLING), 47–54. Barcelona, Spain, December 2020. Association for Computational Linguistics.
