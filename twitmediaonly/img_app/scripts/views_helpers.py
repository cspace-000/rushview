from django.conf import settings


def toggle_display_order(request, display_order):
    tweet_objs = request.session.get('results')    
    if display_order == 'top':
        

        tweet_objs.sort(key=lambda tweet_obj : int(tweet_obj['intlike_count']), reverse=True)

    elif display_order == 'recent':
        tweet_objs.sort(key=lambda tweet_obj : tweet_obj['created_at'], reverse=True)
    
    request.session['results'] = tweet_objs


def get_tweet_obj(request, tweet_id):
     
    results_range = range(len(request.session.get('results')))
    
    tweet_objs = []
    next_tweet = False
    previous_tweet = False
        
    for i in results_range:
        tweet_obj = request.session.get('results')[i]
        
        if tweet_obj['tweet_id'] == tweet_id:
            tweet_objs.append(tweet_obj)
            
            if i-1 in results_range:
                previous_tweet_obj = request.session.get('results')[i-1]
                if previous_tweet_obj['tweet_id'] != tweet_obj['tweet_id']:            
                    previous_tweet = previous_tweet_obj
                
            if i+1 in results_range:
                next_tweet_obj = request.session.get('results')[i+1]
                if next_tweet_obj['tweet_id'] != tweet_obj['tweet_id']:
                    next_tweet = next_tweet_obj
            
    return tweet_objs, previous_tweet, next_tweet



def get_page_obj_page_range(request, page_num):
        page_obj = False
        page_range = False
        
        tweet_objs = request.session.get('results')
        session_list = chunk_objs(tweet_objs)
        if page_num in range(len(session_list)):
        
            page_obj = session_list[page_num]
            page_range = [x for x in range(len(session_list))]
        
    
        return page_obj, page_range
      
       
def chunk_objs(tweet_objs, chunk_size=50):
    #chunks tweet objs into [[images/page1], [images/page2], etc...] 
    #len of chunks is number of pages
    session_list = []
    for i in range(0, len(tweet_objs), chunk_size):
        session_list.append(tweet_objs[i:i+chunk_size])
    return session_list 


def authentication_checker(request):
    authenticated = False
    access_token = None
    access_token_secret = None
    
    if not settings.DEBUG:
        if request.session.get('access_token') and request.session.get('access_token_secret'):
            authenticated = True        
            access_token = request.session.get('access_token')
            access_token_secret = request.session.get('access_token_secret')
            
    else:
        authenticated = True
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET
        
        
    return authenticated, access_token, access_token_secret
    