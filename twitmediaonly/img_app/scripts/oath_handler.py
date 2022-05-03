import tweepy

import urllib.parse
import json

from django.conf import settings

def create_oath1_user_handler():
    authorization_url = None
    oauth_token = None
    error_message = None
    
    try:            
        oauth1_user_handler = tweepy.OAuth1UserHandler(consumer_key = settings.CONSUMER_KEY,
                                                consumer_secret = settings.CONSUMER_SECRET,
                                                callback='https://www.rushview.net/callback')

    except Exception as e:
        print(e)
        error_message = 'Could not load server side authentication.'   
        return authorization_url, oauth_token, error_message
             

    try:
        #authorization_url = oauth1_user_handler.get_authorization_url(signin_with_twitter=False)
        authorization_url = oauth1_user_handler.get_authorization_url()
        parsed_url = urllib.parse.urlparse(authorization_url)
        res = urllib.parse.parse_qs(parsed_url.query)
    
        oauth_token = res['oauth_token'][0]
        oauth_token_secret = oauth1_user_handler.request_token["oauth_token_secret"]
        #print('oauth_token: ', authorization_url)
        
    except Exception as e:
        print(e)
        error_message = 'Could not authenticate you.'
        return authorization_url, oauth_token, error_message
    


    return authorization_url, oauth_token, oauth_token_secret, error_message


def callback_oath1handler(oauth_token, oauth_verifier, oauth_token_secret):    
    access_token = None
    access_token_secret = None    
    error_message = None
    
    try:  
        oauth1_user_handler = tweepy.OAuth1UserHandler(consumer_key = settings.CONSUMER_KEY,
                                                consumer_secret = settings.CONSUMER_SECRET,
                                                callback='https://www.rushview.net/callback')

    except Exception as e:
        print(e)
        error_message = 'Could not load server side authentication.'   
        return access_token, access_token_secret, error_message

    try:
        oauth1_user_handler.request_token = {
            "oauth_token": oauth_token,
            "oauth_token_secret": oauth_token_secret
        }
        
        access_token, access_token_secret = oauth1_user_handler.get_access_token(oauth_verifier)
        
    except Exception as e:
        print(e)
        error_message = 'Could not authenticate you.'   
        return access_token, access_token_secret, error_message
        
    return access_token, access_token_secret, error_message




