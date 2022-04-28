from datetime import datetime
from . import twitter_request, paginator
from .views_helpers import toggle_display_order, get_tweet_obj, get_page_obj_page_range, chunk_objs, authentication_checker

###Context handlers:        
def artist_or_search_context_handler(request, artist_name=None, query=None):    
    context = {}    
    #start_time = datetime.now()
    
    authenticated, access_token, access_token_secret = authentication_checker(request)
    
    if authenticated:   
        context['authenticated'] = True
    
        if artist_name:
            Twit = twitter_request.TwitterRequestArtist(access_token, access_token_secret)
            Twit.main(username = artist_name)      
            
        elif query:
            Twit = twitter_request.TwitterRequestQuery(access_token, access_token_secret)
            Twit.main(query)
            query = query.strip('#')

        else:
            print('ERROR, not artist, not query')
    
    
        if Twit.error:
            print("No results found in Twitter api.")
            #context = {}
    
        else:
            
            request.session['artist_name'] = artist_name
            request.session['query'] = query 

            tweet_objs = Twit.tweet_objs #actually dictionaries
            
            if len(tweet_objs) == 0:
                pass
            #i think if there's a matching username with no media
                #context = {}
                
            else:
                request.session['results'] = tweet_objs

                page_obj, page_range = get_page_obj_page_range(request, 0)
                     
                paginator_obj = paginator.Paginator(page_range, 0)

                
                # end_time = datetime.now()
                # time_delta = end_time - start_time
                # request_time = '{0} second(s)\n{1} microsecond(s)'.format(time_delta.seconds, time_delta.microseconds)
                
                context['artist_name'] = artist_name
                context['query'] = query
                context['page_obj'] = page_obj
                context['paginator'] = paginator_obj
                context['authenticated'] = True
             
    else:
        context['authenticated'] = False
        
    return context


def page_context_handler(request, page_num, artist_name=None, query=None):
    current_params = ''
    display_order = ''
    
    authenticated, access_token, access_token_secret = authentication_checker(request)
    
    if authenticated:   
        context = {'authenticated': True, 
                    }
    
        # if request.GET:
            # current_params = '?' + request.GET.urlencode()
            
        if request.method == 'GET':
            current_params = '?' + request.GET.urlencode()
            if request.GET.get('order'):
                display_order = request.GET['order']
                toggle_display_order(request, display_order)            
                

        page_obj, page_range = get_page_obj_page_range(request, page_num)
        
        #print('page_context_handler: ', query)
        if page_obj != False and request.session.get('results') != False:
            paginator_obj = paginator.Paginator(page_range, page_num)
            context = {'artist_name' : artist_name,
                        'query': query,
                        'page_obj': page_obj,
                        'paginator': paginator_obj,

                        'current_params': current_params,
                        'display_order': display_order,
                        'authenticated': True,
                        }
        
        else:    
            context = {'artist_name' : artist_name,
                        'query': query,
                        'page_obj': False,
                        }

    else:
        context = {'authenticated': False, 
                    }

    return context
