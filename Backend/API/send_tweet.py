import tweepy
import requests
import json

consumer_key = 'JDdj6I1S1WqU7p5nYs3OMisxK'
consumer_secret_key = 'Gwtcqqge1qLnhgK3uMKpVOhefUSKwMtk5XR4oYpXLy8ppYwad8'
access_token = '3154027043-aCioPGK5Lxynw6bFQcB9RmlCX3EoMSe0XeXnv1S'
access_token_secret = 'Carqdl4m66kygEYmUhUJSt3nP3czOrXKQLCbTxTodDfWZ'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJnPVAEAAAAAW7hAlkRMbEdjwg9bPmjabfExBdM%3Dk0pBQPQZiPQWDD8zIC631AhW1LFWyLvvJVjqY2EHiybNpwqwHR'


def send_tweet(commentaar):
    # variables for accessing twitter API
    # Using the tweepy api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    status = api.update_status(commentaar)
    status_dct = status._json
    tweet_id = status_dct.get('id')

    return tweet_id


def get_tweets():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.user_timeline(
        screen_name='@maurice_stoof',
        # 200 is the maximum allowed count
        count=200,
        include_rts=False,
        # Necessary to keep full_text
        # otherwise only the first 140 words are extracted
        tweet_mode='extended'
    )
    print(tweets[:3])

    return tweets[:3]


if __name__ == '__main__':
    tweet = get_tweets()
    print(tweet)
