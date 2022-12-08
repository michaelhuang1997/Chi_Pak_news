import numpy as np
import pandas as pd
import tweepy as tw
from tqdm import tqdm

consumer_api_key="JcrxIFV9qiPsEERpTQtwnwdQl"
consumer_api_secret="xuHfLGXnHzOBQA3duwxsXPBx0e4uXeZxqAqTsYvY25y4FDFX7U"
access_token= '3442624097-s4Wyi9bCEFPoYA6yEegHP6XvZRuFgFWAAqwU4rE'
access_token_secret= 'z7UYfJCef6DgyKp8tizEljmQDjvrfvfjmooBsOvZ9tGdD'

auth = tw.OAuthHandler(consumer_api_key, consumer_api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words="pakistan"
since = "2000-01-01"
until="2020-08-20"
tweets = tw.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              until=until     
              ).items(7500)

tweets_copy = []
for tweet in tqdm(tweets):
    tweets_copy.append(tweet)

print(f"New tweets retrieved: {len(tweets_copy)}")

tweets_df = pd.DataFrame()
for tweet in tqdm(tweets_copy):
    hashtags = []
    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
    except:
        pass
    tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,\
                                               'user_description': tweet.user.description,
                                               'user_created': tweet.user.created_at,
                                               'user_followers': tweet.user.followers_count,
                                               'user_friends': tweet.user.friends_count,
                                               'user_favourites': tweet.user.favourites_count,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': tweet.text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source,
                                               'is_retweet': tweet.retweeted}, index=[0]))

tweets_df.to_csv('pak.csv',index=False)