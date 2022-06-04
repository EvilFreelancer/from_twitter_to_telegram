import os
import pickle
import time

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

import twython as Twython
from dotenv import load_dotenv

load_dotenv()

# Read all variables
tw_username = os.getenv('TWITTER_USER_NAME')
tw_key = os.getenv('TWITTER_API_KEY')
tw_secret = os.getenv('TWITTER_API_KEY_SECRET')
tw_oauth_token = os.getenv('TWITTER_ACCESS_TOKEN')
tw_oauth_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
tg_channel_name = os.getenv('TELEGRAM_CHANNEL_NAME')
tg_token = os.getenv('TELEGRAM_TOKEN')

api = Twython.Twython(tw_key, tw_secret, tw_oauth_token, tw_oauth_secret)


def first_run():
    file_exists = os.path.exists('sav.p')
    if file_exists is False:
        user_timeline = api.get_user_timeline(
            screen_name=tw_username,
            # This 'count' is how many tweets back from the most recent tweet that will be forwarded to telegram
            count=2
        )
        tweet_id = user_timeline[1]['id']
        file_pickle(tweet_id)


def get_timeline(tweet_id):
    user_timeline = api.get_user_timeline(screen_name=tw_username, since_id=tweet_id)
    return user_timeline


def read_latest_id():
    line = file_unpickle()
    if len(str(line)) < 2:
        return 0
    else:
        return line


def send_message(msg):
    msg = quote(msg, safe='')
    link = 'https://api.telegram.org/bot' \
           + tg_token \
           + '/sendMessage?chat_id=@' \
           + tg_channel_name \
           + '\&text="' \
           + msg \
           + '"'
    os.system('curl ' + link)


def file_pickle(var):
    pickle.dump(var, open("sav.p", "wb"))


def file_unpickle():
    saved = pickle.load(open('sav.p', "rb"))
    return saved


def main():
    latest_tweet_id = read_latest_id()
    user_timeline = get_timeline(latest_tweet_id)
    number_of_tweets = len(user_timeline)
    if number_of_tweets > 0:
        for i in reversed(range(0, number_of_tweets)):
            if user_timeline[i]['text']:
                print(user_timeline[i]['text'])
                send_message(user_timeline[i]['text'] + "\n\n#twitter")
                time.sleep(4)
        latest_tweet_id = user_timeline[0]['id']
    file_pickle(latest_tweet_id)


first_run()
main()
