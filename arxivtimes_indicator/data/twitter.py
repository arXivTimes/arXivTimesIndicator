import os
import urllib.request
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
    tweets = [status for status in tweepy.Cursor(api.user_timeline).items()]

    # tweets = api.user_timeline(screen_name='arxivtimes', count=count, tweet_mode='extended')

    return tweets


def get_full_url(short_url):
    try:
        full_url = urllib.request.urlopen(short_url).geturl()
    except:
        full_url = ''
    return full_url


def rank_paper(tweets):
    paper_rank = []
    for tweet in tweets:
        short_url = tweet.text.split(' ')[-1]
        url = get_full_url(short_url)
        if not url.startswith('https://github.com/arXivTimes/arXivTimes/issues/'):
            continue
        favorite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count
        score = favorite_count + 5 * retweet_count
        paper_rank.append((score, url))

    scores = [s for s, _ in paper_rank]
    urls = [u for _, u in paper_rank]
    scores = std_score(scores)

    return scores, urls
