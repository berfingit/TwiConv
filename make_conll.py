# Annalena Kohnert

import os
import sys
import re
import copy


def main():
    conll_skeleton = 'conll_skeleton/'
    conll = 'conll/'
    diff = 'diff/'
    tweets = sys.argv[1]
    authors = sys.argv[2]

    if not os.path.isdir(conll):
        os.mkdir(conll)

    for filename in os.listdir(conll_skeleton):
        skeleton = open(conll_skeleton+filename, 'r')
        new_conll = open(conll+filename, 'w')
        previous_tweet = '000'
        for line in skeleton:
            if line[0] == '#' or line == '\n':
                new_conll.write(line)
            else:
                tweet = line.split()[-1]
                if tweet != previous_tweet:
                    tweet_missing = False

                    try:
                        t = open(os.path.join(tweets, tweet+'.txt'), 'r')
                    except:
                        print('WARNING: The tweet with ID {} is missing'.format(tweet))
                        tweet_missing = True

                    try:
                        a = open(os.path.join(authors, tweet+'.txt'), 'r')
                        username = a.read().strip('\n')
                    except:
                        print('WARNING: The tweet with ID {} is available, but not its author. Make sure that you correctly added the author text file.'.format(tweet))
                        username = '_'

                    if not tweet_missing:
                        d = open(diff+tweet+'.txt', 'r')
                        y = d.read().split('\n')
                        untokenized = t.read().split()

                        splits = [i for i, x in enumerate(y) if re.match(r"^[0-9].*(c|d|a).*[0-9]$", x)]
                        splits.append(len(y))
                        tokenization_steps = []

                        for i in range(len(splits)-1):
                            start = splits[i]
                            end = splits[i+1]
                            tokenization_steps.append(y[start:end])
                        tokenizer = dict()
                        added_tokens = dict()
                        deleted_tokens = dict()

                        for step in tokenization_steps:
                            for i in range(len(step)):
                                if len(step[i].split()) > 1:
                                    step[i] = step[i].split()[1]

                            if 'c' in step[0]:
                                original_token_no = step[0].split('c')[1].split(',')

                            tokens_added = False
                            if 'd' in step[0]:
                                tokens_added = True
                                original_token_no = step[0].split('d')[1].split(',')
                                added_tokens[int(original_token_no[0])] = step[1:]

                            tokens_deleted = False
                            if 'a' in step[0]:
                                tokens_deleted = True
                                original_token_no = step[0].split('a')[1].split(',')
                                for i, tok in enumerate(original_token_no):
                                    deleted_tokens[int(tok)] = step[1:][i]

                            temp = [i for i, x in enumerate(step) if x == '---']
                            if temp != []:
                                split = temp[0]
                            post_tokenization = step[1:split]

                            if not tokens_added and not tokens_deleted:
                                if len(original_token_no) == 1:
                                    tokenizer[int(original_token_no[0])-1] = post_tokenization
                                else:
                                    tokenizer[int(original_token_no[0])-1] = post_tokenization
                                    for tok in range(int(original_token_no[0]), int(original_token_no[1])):
                                        tokenizer[tok] = ''


                        tokenized = []

                        if tokenizer or added_tokens or deleted_tokens:
                            for i in range(len(untokenized)):
                                if i in added_tokens:
                                    tokenized += added_tokens[i]
                                if i in tokenizer:
                                    if tokenizer[i] != '':
                                        tokenized += tokenizer[i]
                                else:
                                    tokenized.append(untokenized[i])
                                if i in deleted_tokens:
                                    if i+1 not in deleted_tokens:
                                        tok = tokenized[-1]
                                    tokenized = tokenized[:-1]
                                    tokenized[-1] = tok
                        else:
                            tokenized = untokenized


                if tweet_missing:
                    new_conll.write(line)
                else:
                    if len(tokenized) > 0:
                        line_copy = copy.deepcopy(line.split())
                        line_copy[3] = tokenized[0]
                        new_line = line_copy[:-1]
                        new_line[6] = username
                        new_conll.write('\t'.join(new_line)+'\n')
                        tokenized.pop(0)

                previous_tweet = tweet

        skeleton.close()
        new_conll.close()

if __name__ == "__main__":
    main()
