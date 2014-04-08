from tweepy import StreamListener
import time, tweepy, sys
import json, time, sys

class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        self.output  = open(fprefix + '.' 
                            + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.delout  = open('delete.txt', 'a')

    def on_data(self, data):

        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return false

    def on_status(self, status):
        self.output.write(status + "\n")

        self.counter += 1

        if self.counter >= 20000:
            self.output.close()
            self.output = open('../streaming_data/' + self.fprefix + '.' 
                               + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0

        return

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 

## authentication
consumer_key = '1LA3dSIQib3f9daT5capcrdnJ'
consumer_key_secret = 'Un9RVQf0TSpOgvEcSGEE0QcYR5R1Kk9xaGXmCWOe6joXYmaC7H'
access_token = '337439389-nDmBgIrySv6oiedVDVBNhYZ1gnnPFBomBAUsLoph'
access_token_secret = 'OSO3BRSDdf7QKOorPoN9sPWhMFXwCazMwPvuXDhpENa6x'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def main():
    track = ['vaccination', 'vaccine', 'vaccinated', 'vaccinate', 'vaccinating', 'immunized', 'immunization', 'immunizing']
 
    listen = SListener(api, 'myprefix')
    stream = tweepy.Stream(auth, listen)

    print "Streaming started..."

    try: 
        stream.filter(track = track)
    except:
        print "error!"
        stream.disconnect()

if __name__ == '__main__':
    main()