#!/usr/bin/env python

import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

import json
from insert_dict import insert_record

"""
Parse a tweet as emitted by the twitter API.
"""

json_data = open(file)

tweet_json = """
{"created_at":"Mon Apr 07 02:58:43 +0000 2014","id":453003909104422914,"id_str":"453003909104422914","text":"RT @CTV_AvisFavaro: Old diseases and their new victims - #measles & #meningitis and their devastating effects @usatoday http:\/\/t.co\/snbNJe","source":"web","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":32922549,"id_str":"32922549","name":"Joe Troxler","screen_name":"joetea48","location":"","url":null,"description":"Writer\/storyteller\/researcher, communicator, broadcaster, media relations advisor, political junkie, special events","protected":false,"followers_count":827,"friends_count":2001,"listed_count":41,"created_at":"Sat Apr 18 15:57:25 +0000 2009","favourites_count":44643,"utc_offset":-18000,"time_zone":"Central Time (US & Canada)","geo_enabled":false,"verified":false,"statuses_count":70068,"lang":"en","contributors_enabled":false,"is_translator":false,"is_translation_enabled":false,"profile_background_color":"C0DEED","profile_background_image_url":"http:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_image_url_https":"https:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_tile":false,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/3255195828\/eacd722fd70c90316ce1beb0d2da2c88_normal.jpeg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/3255195828\/eacd722fd70c90316ce1beb0d2da2c88_normal.jpeg","profile_link_color":"0084B4","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"retweeted_status":{"created_at":"Mon Apr 07 02:36:19 +0000 2014","id":452998272396042240,"id_str":"452998272396042240","text":"Old diseases and their new victims - #measles & #meningitis and their devastating effects @usatoday http:\/\/t.co\/snbNJe7gJB","source":"web","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":24185568,"id_str":"24185568","name":"Avis Favaro","screen_name":"CTV_AvisFavaro","location":"Toronto","url":"http:\/\/www.ctv.ca\/health\/","description":"Medical Correspondent CTV National News and network hypochondriac","protected":false,"followers_count":5487,"friends_count":620,"listed_count":227,"created_at":"Fri Mar 13 15:08:07 +0000 2009","favourites_count":19,"utc_offset":-14400,"time_zone":"Eastern Time (US & Canada)","geo_enabled":false,"verified":false,"statuses_count":4056,"lang":"en","contributors_enabled":false,"is_translator":false,"is_translation_enabled":false,"profile_background_color":"080008","profile_background_image_url":"http:\/\/pbs.twimg.com\/profile_background_images\/189069127\/twitter_avis_favaro2.jpg","profile_background_image_url_https":"https:\/\/pbs.twimg.com\/profile_background_images\/189069127\/twitter_avis_favaro2.jpg","profile_background_tile":false,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/2431981210\/zmfkc4mpymnj5g61f56g_normal.jpeg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/2431981210\/zmfkc4mpymnj5g61f56g_normal.jpeg","profile_link_color":"0084B4","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"080808","profile_use_background_image":true,"default_profile":false,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"retweet_count":2,"favorite_count":0,"entities":{"hashtags":[{"text":"measles","indices":[37,45]},{"text":"meningitis","indices":[53,64]}],"symbols":[],"urls":[{"url":"http:\/\/t.co\/snbNJe7gJB","expanded_url":"http:\/\/www.usatoday.com\/story\/news\/nation\/2014\/04\/06\/anti-vaccine-movement-is-giving-diseases-a-2nd-life\/7007955\/?sf24712242=1","display_url":"usatoday.com\/story\/news\/nat","indices":[105,127]}],"user_mentions":[{"screen_name":"USATODAY","name":"USA TODAY","id":15754281,"id_str":"15754281","indices":[95,104]}]},"favorited":false,"retweeted":false,"possibly_sensitive":false,"lang":"en"},"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[{"text":"measles","indices":[57,65]},{"text":"meningitis","indices":[73,84]}],"symbols":[],"urls":[{"url":"http:\/\/t.co\/snbNJe7gJB","expanded_url":"http:\/\/www.usatoday.com\/story\/news\/nation\/2014\/04\/06\/anti-vaccine-movement-is-giving-diseases-a-2nd-life\/7007955\/?sf24712242=1","display_url":"usatoday.com\/story\/news\/nat","indices":[143,144]}],"user_mentions":[{"screen_name":"CTV_AvisFavaro","name":"Avis Favaro","id":24185568,"id_str":"24185568","indices":[3,18]},{"screen_name":"USATODAY","name":"USA TODAY","id":15754281,"id_str":"15754281","indices":[115,124]}]},"favorited":false,"retweeted":false,"possibly_sensitive":false,"filter_level":"medium","lang":"en"}
"""


obj = json.loads(tweet_json)

tweet = dict()
user = dict()

tweet['tweet_id'] = obj['id']
tweet['user_id'] = obj['user']['id']
tweet['text'] = obj['text']
tweet['created_at'] = obj['created_at']

user['user_id'] = obj['user']['id']
user['user_name'] = obj['user']['screen_name']
user['location'] = obj['user']['location']

insert_record(tweet, 'tweets_2014')
insert_record(user, 'users_2014')
