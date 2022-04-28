import tweepy, json
from django.conf import settings

class TwitterRequestBase():
    def __init__(self, access_token, access_token_secret):
        
        #self.username = username
        self.access_token = access_token
        self.access_token_secret = access_token_secret       
        
        self.tweet_objs = []
        self.error = False
        
        self.create_client()
        # try:
            # auth = self.load_auth()
            # self.client=tweepy.Client(
                # bearer_token=auth['bearer_token'],
                # consumer_key=auth['consumer_key'],
                # consumer_secret=auth['consumer_secret'],
                # access_token=access_token, 
                # access_token_secret=access_token_secret
            # )


        # except Exception as e:
            # self.error = True
            # print(e)
            # print('Error creating Tweepy client')


    def create_client(self):
    
        try:
            self.client = tweepy.Client(
                bearer_token = settings.BEARER_TOKEN,
                consumer_key = settings.CONSUMER_KEY,
                consumer_secret = settings.CONSUMER_SECRET,
                access_token = self.access_token, 
                access_token_secret = self.access_token_secret
            )


        except Exception as e:
            self.error = True
            print(e)
            print('Error creating Tweepy client')
            
        


    def main(self):
        pass                
   
    # def load_auth(self, path ='keys.txt'):
    # # def load_auth(self, path ='keys.txt'):
        # with open(path, 'r') as f:
            # return json.loads(f.read())
   
    def get_tweets(self):
        pass
    
    
    def get_tweet(self):
        pass
    
    def process_tweets(self, tweets):
        href_links_vid_id = {} #for mapping media_key to tweet_id to get public_metrics, {media_key, [tweet_data]}
        username_mapper = {} # for mapping author_id, username {author_id, username}

        if 'users' in tweets.includes:
            for user in tweets.includes['users']:
                username_mapper[user.id] = [user.username,
                                            user.description]

        
        for tweet in tweets.data:
            if tweet.attachments:
                if 'media_keys' in tweet.attachments:
                    tweet_id = tweet.id
                    like_count = self.thousand_converter(tweet.public_metrics['like_count'])
                    retweet_count = self.thousand_converter(tweet.public_metrics['retweet_count'])
                    reply_count = self.thousand_converter(tweet.public_metrics['reply_count'])
                    # tweet_text = tweet.text[0:50]
                    tweet_text = tweet.text
                    author_id = tweet.author_id
                    created_at = tweet.created_at.timestamp() #comes in datetime.datetime
                    intlike_count = tweet.public_metrics['like_count']
                    username = username_mapper[tweet.author_id][0]
                    description = username_mapper[tweet.author_id][1]

                    #Need to iterate if multiple pics in one tweet
                    for i in range(len(tweet.attachments['media_keys'])):
                        href_links_vid_id[tweet.attachments['media_keys'][i]] = [tweet_id, 
                                                                            like_count,
                                                                            retweet_count,
                                                                            reply_count,
                                                                            tweet_text,
                                                                            author_id,
                                                                            created_at,
                                                                            intlike_count,
                                                                            username,
                                                                            description]      


        if 'media' in tweets.includes:
            for media in tweets.includes['media']: 
                if media.media_key in href_links_vid_id: #for mapping media_key to tweet_id to get public_metrics
                    tweet_id, like_count, retweet_count, reply_count, tweet_text, author_id, created_at, intlike_count, username, description = href_links_vid_id[media.media_key]

                    if media.type == 'photo':
                        href = media.url + '?format=jpg&name=large'
                        thumbnail = media.url                       
                    
                    elif media.type == 'video' or media.type == 'animated_gif':
                        #href = 'https://twitter.com/{0}/status/{1}'.format(self.username, tweet_id)
                        href = 'https://twitter.com/{0}/status/{1}'.format('x', tweet_id)
                        thumbnail = media.preview_image_url
                        
                    
                    else:
                        print('Error process_tweets, unknown type: ' + media.type)
                        #unknown media type
                    tweet_obj = {}
                    tweet_obj['href'] = href
                    tweet_obj['thumbnail'] = thumbnail
                    tweet_obj['tweet_id'] = tweet_id
                    tweet_obj['like_count'] = like_count
                    tweet_obj['retweet_count'] = retweet_count
                    tweet_obj['reply_count'] = reply_count
                    tweet_obj['media_type'] = media.type
                    tweet_obj['tweet_text'] = tweet_text
                    tweet_obj['author_id'] = author_id
                    tweet_obj['created_at'] = created_at
                    tweet_obj['intlike_count'] = intlike_count
                    tweet_obj['username'] = username
                    tweet_obj['description'] = description
                                        
                    self.tweet_objs.append(tweet_obj)

                
                else:
                    print("No media key found in href_links_vid_id.") 
                    self.error = True
                                    
    def process_tweet(self, tweet):
        href_links_vid_id = {} #for mapping media_key to tweet_id to get public_metrics, {media_key, [tweet_data]}
        username_mapper = {} # for mapping author_id, username {author_id, username}

        if 'users' in tweet.includes:
            for user in tweet.includes['users']:
                username_mapper[user.id] = [user.username,
                                            user.description]

        

        if tweet.data.attachments:
            if 'media_keys' in tweet.data.attachments:
                tweet_id = tweet.data.id
                like_count = self.thousand_converter(tweet.data.public_metrics['like_count'])
                retweet_count = self.thousand_converter(tweet.data.public_metrics['retweet_count'])
                reply_count = self.thousand_converter(tweet.data.public_metrics['reply_count'])
                # tweet_text = tweet.data.text[0:50]
                tweet_text = tweet.data.text
                author_id = tweet.data.author_id
                created_at = tweet.data.created_at.timestamp() #comes in datetime.datetime
                intlike_count = tweet.data.public_metrics['like_count']
                username = username_mapper[tweet.data.author_id][0]
                description = username_mapper[tweet.data.author_id][1]

                #Need to iterate if multiple pics in one tweet
                for i in range(len(tweet.data.attachments['media_keys'])):
                    href_links_vid_id[tweet.data.attachments['media_keys'][i]] = [tweet_id, 
                                                                        like_count,
                                                                        retweet_count,
                                                                        reply_count,
                                                                        tweet_text,
                                                                        author_id,
                                                                        created_at,
                                                                        intlike_count,
                                                                        username,
                                                                        description]      


        if 'media' in tweet.includes:
            for media in tweet.includes['media']: 
                if media.media_key in href_links_vid_id: #for mapping media_key to tweet_id to get public_metrics
                    tweet_id, like_count, retweet_count, reply_count, tweet_text, author_id, created_at, intlike_count, username, description = href_links_vid_id[media.media_key]

                    if media.type == 'photo':
                        href = media.url + '?format=jpg&name=large'
                        thumbnail = media.url                       
                    
                    elif media.type == 'video' or media.type == 'animated_gif':
                        #href = 'https://twitter.com/{0}/status/{1}'.format(self.username, tweet_id)
                        href = 'https://twitter.com/{0}/status/{1}'.format('x', tweet_id)
                        thumbnail = media.preview_image_url
                        
                    
                    else:
                        print('Error process_tweets, unknown type: ' + media.type)
                        #unknown media type
                    tweet_obj = {}
                    tweet_obj['href'] = href
                    tweet_obj['thumbnail'] = thumbnail
                    tweet_obj['tweet_id'] = tweet_id
                    tweet_obj['like_count'] = like_count
                    tweet_obj['retweet_count'] = retweet_count
                    tweet_obj['reply_count'] = reply_count
                    tweet_obj['media_type'] = media.type
                    tweet_obj['tweet_text'] = tweet_text
                    tweet_obj['author_id'] = author_id
                    tweet_obj['created_at'] = created_at
                    tweet_obj['intlike_count'] = intlike_count
                    tweet_obj['username'] = username
                    tweet_obj['description'] = description
                                        
                    self.tweet_objs.append(tweet_obj)

                
                else:
                    print("No media key found in href_links_vid_id.") 
                    self.error = True   
                    
    def final_error_check(self):
        if len(self.tweet_objs) == 0:
            self.error = True
                           
    def thousand_converter(self, num):
    #converts high num into num.k and str
        if num > 1000:
            num /= 1000
            num = round(num, 1)
            return str(num) + "k"
        else:
            return str(num)
    
        
class TwitterRequestArtist(TwitterRequestBase):
    def __init__(self, access_token, access_token_secret):
        super().__init__(access_token, access_token_secret)

    def main(self, username):
        try:
            if type(username) == int:
                author_id = username
            else:            
                author_id = self.client.get_user(username=username).data.id            
            if author_id:
                next_token = True
                pagination_token = False
                
                while next_token:
                    tweets, next_token = self.get_tweets(author_id, pagination_token)
                    self.process_tweets(tweets)
                    pagination_token = next_token
                    
            self.final_error_check()
        except Exception as e:
            self.error = True
            print(e)
            
    def get_tweets(self, author_id, pagination_token=False):       
        if pagination_token:            
            tweets= self.client.get_users_tweets(id=author_id, 
                                                        exclude=['retweets', 'replies'],
                                                        tweet_fields =['public_metrics', 'author_id', 'created_at'],                    
                                                        media_fields=['height','width','url','preview_image_url'], 
                                                        expansions=['attachments.media_keys', 'author_id'],
                                                        user_fields = ['id', 'username', 'description'],
                                                        max_results=100,
                                                        pagination_token=pagination_token
                                                        )
        else:
            tweets= self.client.get_users_tweets(id=author_id, 
                                                exclude=['retweets', 'replies'],  
                                                tweet_fields =['public_metrics', 'author_id', 'created_at'],
                                                media_fields=['height','width','url','preview_image_url'], 
                                                expansions=['attachments.media_keys', 'author_id'],
                                                user_fields = ['id', 'username', 'description'],
                                                max_results=100
                                                )

        if 'next_token' in tweets.meta:
            next_token = tweets.meta['next_token']
        else:
            next_token = False
        return tweets, next_token
    
                

class TwitterRequestQuery(TwitterRequestBase):
    def __init__(self, access_token, access_token_secret):
        super().__init__(access_token, access_token_secret)
        
    def main(self, query):
        query += ' has:media -is:retweet -is:reply'
        
        try:
            
            total_requests = 0
            next_token = True
            pagination_token = False
            
            
            #while next_token and total_requests < 4:
            while next_token:
                if total_requests < 4:
                    tweets, next_token, total_requests = self.get_tweets(query, total_requests, pagination_token)
                    self.process_tweets(tweets)
                    pagination_token = next_token
                else:
                    break
                    
            self.final_error_check()
        except Exception as e:
            self.error = True
            print(e)
    

    def get_tweets(self, query, total_requests, pagination_token=False):        
        if pagination_token:        
            tweets = self.client.search_recent_tweets(query=query, 
                                                        #exclude=['retweets', 'replies'],
                                                        tweet_fields =['public_metrics', 'author_id', 'created_at'],                    
                                                        media_fields=['height','width','url','preview_image_url'], 
                                                        expansions=['attachments.media_keys', 'author_id'],
                                                        user_fields = ['id', 'username', 'description'],
                                                        max_results=100,
                                                        next_token=pagination_token
                                                        )
        else:
            tweets= self.client.search_recent_tweets(query=query, 
                                                #exclude=['retweets', 'replies'],  
                                                tweet_fields =['public_metrics','author_id', 'created_at'],
                                                media_fields=['height','width','url','preview_image_url'], 
                                                expansions=['attachments.media_keys', 'author_id'],
                                                user_fields = ['id', 'username','description'],
                                                max_results=100
                                                )
        if 'next_token' in tweets.meta:
            next_token = tweets.meta['next_token']
        else:
            next_token = False        
        total_requests += 1        
        return tweets, next_token, total_requests
     


class TwitterRequestTweet(TwitterRequestBase):
    def __init__(self, access_token, access_token_secret):
        super().__init__(access_token, access_token_secret)   
    
    def main(self, tweet_id):
        try:
            tweet = self.get_tweet(tweet_id)
            self.process_tweet(tweet)
            self.final_error_check()
        
        except Exception as e:
            self.error = True
            print(e)
            
    def get_tweet(self, tweet_id):
        tweet = self.client.get_tweet(tweet_id,
                                    tweet_fields =['public_metrics', 'author_id', 'created_at'],                    
                                    media_fields=['height','width','url','preview_image_url'], 
                                    expansions=['attachments.media_keys', 'author_id'],
                                    user_fields = ['id', 'username', 'description']
                                    )
                                    
        return tweet
        


if __name__ == "__main__":
    print('stat')
    