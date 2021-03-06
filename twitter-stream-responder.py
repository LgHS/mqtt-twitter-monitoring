from twitter import *
import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

sleep_time = 1

#### Load our API credentials  ####

# Python2:
# config = {}
# execfile("config.py", config)

# Python3:
config = {}
with open("config.py") as f:
    code = compile(f.read(), "config.py", 'exec')
    exec(code, config)

#######################

auth = OAuth(
    config["access_key"],
    config["access_secret"],
    config["consumer_key"],
    config["consumer_secret"]
)
twitter = Twitter(auth=auth)
stream = TwitterStream(
    domain="userstream.twitter.com",
    auth=auth,
    secure=True
)

tweet_iter = stream.user()

for tweet in tweet_iter:
    time.sleep(sleep_time)
    
    try:
        print(tweet)
    except UnicodeEncodeError:
        # Failsafe for Windows :)
        print('Can\'t print that!')
    
    print()
    
    if 'event' in tweet and tweet['event'] == 'follow':
        print('NEW FOLLOWER "{}"'.format(tweet['source']['name']))
        print()
        
        publish.single(
            config['blink'],
            '2',
            hostname=config['mqtt_hostname'],
            port=config['mqtt_port']
        )
    
    if 'entities' in tweet:
        mentions = (mention['screen_name'] for mention in tweet['entities']['user_mentions'])
        
        if config['mention_monitore'] in mentions:            
            print('MENTION')
            
            publish.single(
                config['blink'],
                '2',
                hostname=config['mqtt_hostname'],
                port=config['mqtt_port']
            )
