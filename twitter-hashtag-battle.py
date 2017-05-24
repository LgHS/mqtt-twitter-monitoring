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
stream = TwitterStream(auth=auth, secure=True)
tweet_iter = stream.statuses.filter(track=config['track'])

for tweet in tweet_iter:
    time.sleep(1)
    
    try:
        print(tweet['text'])
    except UnicodeEncodeError:
        # Failsafe for Windows :)
        print('Can\'t print that!')
    
    if config['track'].split(',')[0] in tweet['text'].lower():
        print('GREEN')
        publish.single(
            config['green_light'],
            '1',
            hostname=config['mqtt_hostname'],
            port=config['mqtt_port']
        )
        time.sleep(1)
        publish.single(
            config['green_light'],
            '0',
            hostname=config['mqtt_hostname'],
            port=config['mqtt_port']
        )
    elif config['track'].split(',')[1] in tweet['text'].lower():
        print('RED')
        publish.single(
            config['red_light'],
            '1',
            hostname=config['mqtt_hostname'],
            port=config['mqtt_port']
        )
        time.sleep(1)
        publish.single(
            config['red_light'],
            '0',
            hostname=config['mqtt_hostname'],
            port=config['mqtt_port']
        )
    
    print()