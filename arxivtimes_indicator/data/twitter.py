import os
from datetime import datetime

import tweepy

from arxivtimes_indicator.data.utils import std_score


def load_keys():
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    access_token = os.environ.get('ACCESS_TOKEN')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
    return consumer_key, consumer_secret, access_token, access_token_secret


def fetch_tweets(name='arxivtimes', count=100):
    consumer_key, consumer_secret, access_token, access_token_secret = load_keys()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='arxivtimes', count=100)

    return tweets


def rank_paper(tweets):
    paper_rank = []
    #now = datetime.now()
    for tweet in tweets:
        if tweet.source != 'IFTTT':
            continue

        #created_at = tweet.created_at
        paper_title = ' '.join(tweet.text.split()[:-1])
        favorite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count
        score = favorite_count + 2 * retweet_count
        paper_rank.append((score, paper_title))
        #if now.year == created_at.year and now.month == created_at.month:
        #    paper_rank.append((score, paper_title))
        #else:
        #    paper_rank.append((score, paper_title))

    scores = [s for s, _ in paper_rank]
    titles = [t for _, t in paper_rank]
    scores = std_score(scores)

    return scores, titles
