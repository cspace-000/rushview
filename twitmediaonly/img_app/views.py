from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
#from django.core.paginator import Paginator
import json, math

from django.urls import reverse
from .scripts import twitter_request, paginator

from .scripts.views_context_handlers import artist_or_search_context_handler, page_context_handler
from .scripts.views_helpers import toggle_display_order, get_tweet_obj, authentication_checker
from .scripts.oath_handler import create_oath1_user_handler, callback_oath1handler

#from datetime import datetime

### HTML pointers:
def index(request):
    context = {}
    
    authenticated, _, _ = authentication_checker(request)
    if authenticated:
        context['authenticated'] = True

    return render(request, 'img_app/index.html', context)
    

def artist(request, artist_name):
    if artist_name.startswith('@'):
        artist_name = artist_name.strip('@')
         
    context = artist_or_search_context_handler(request, artist_name=artist_name)
    return render(request, 'img_app/query.html', context)
       
def search(request, query):        

    context = artist_or_search_context_handler(request, query=query)    
    return render(request, 'img_app/query.html', context)

def post_redirect(request):
    ### handles searchbar form
    authenticated, _, _ = authentication_checker(request)
    if authenticated:
        context = {'authenticated' :True}
        
        if request.method=='POST':
            if request.POST.get('artist_name'):
                artist_name = request.POST['artist_name']
                
                if artist_name.startswith('@'):
                    artist_name = artist_name.strip('@')             
                return HttpResponseRedirect(reverse('img_app:artist', args=(artist_name,)))
                           
                
            elif request.POST.get('query'):
                query = request.POST['query']            
                return HttpResponseRedirect(reverse('img_app:search', args=(query,)))   
        
            else:
                #empty search
                #context = {}
                return render(request, 'img_app/query.html', context)
        
        else:
            
                   
            return render(request, 'img_app/query.html', context)
            
    else:
        context = {}       
        return render(request, 'img_app/query.html', context)
        
    
   
def a_page(request, artist_name, page_num):
    ### for pagination with artist search
    if artist_name.startswith('@'):
        artist_name = artist_name.strip('@')
    
    if request.session.get('artist_name') != artist_name:
        return HttpResponseRedirect(reverse('img_app:artist', args=(artist_name,))) 
    
    context = page_context_handler(request, page_num, artist_name=artist_name)
    return render(request, 'img_app/query.html', context)


def q_page(request, query, page_num):
        
    if request.session.get('query') != query:
        return HttpResponseRedirect(reverse('img_app:search', args=(query,))) 
        
    context = page_context_handler(request, page_num, query=query)
    return render(request, 'img_app/query.html', context)


def post(request, tweet_id): 
    current_params = ''
    previous_tweet = ''
    next_tweet = ''
    author_id = ''
    artist_name = ''
    session_name = ''
    query= ''

    authenticated, access_token, access_token_secret = authentication_checker(request)
    
    if authenticated:   
        context = {'authenticated': True, 
                    }
    
        if request.session.get('results'):
            if request.method == 'GET':
                current_params = '?' + request.GET.urlencode()   

                if request.GET.get('order'):
                    display_order = request.GET['order']
                    toggle_display_order(request, display_order)  
                        
            tweet_objs, previous_tweet, next_tweet = get_tweet_obj(request, tweet_id)
            
            
            if len(tweet_objs)==0:
                #name exists but no tweet objects
                Twit = twitter_request.TwitterRequestTweet(access_token, access_token_secret)
                Twit.main(tweet_id)
                if Twit.error:
                    #context = {}
                    return render(request, 'img_app/post.html', context)
                    
            
                else:
                    tweet_objs = Twit.tweet_objs #actually dictionaries

        else:
            Twit = twitter_request.TwitterRequestTweet(access_token, access_token_secret)
            Twit.main(tweet_id)
            if Twit.error:
                #context = {}
                return render(request, 'img_app/post.html', context)
                
            else:
                tweet_objs = Twit.tweet_objs #actually dictionaries
            
        if request.session.get('artist_name'):
            session_name = request.session.get('artist_name')
            
        elif request.session.get('query'):
            query = request.session.get('query')
            
        author_id = tweet_objs[0]['author_id']
        username = tweet_objs[0]['username'] 
        tweet_text = tweet_objs[0]['tweet_text']
        tweet_id= tweet_objs[0]['tweet_id']
        
        context= {'tweet_objs' : tweet_objs,
                    'previous_tweet': previous_tweet,
                    'next_tweet': next_tweet,
                    'author_id': author_id,
                    'artist_name': username,
                    'current_params': current_params,
                    'tweet_text': tweet_text,
                    'tweet_id': tweet_id,
                    'session_name':session_name,
                    'query': query,
                    'authenticated': True,
                    
                    }
    else:
        context = {'authenticated': False, 
                    }
        
    return render(request, 'img_app/post.html', context)
    

def about(request):
    return render(request, 'img_app/about.html')


def search_help(request):
    return render(request, 'img_app/search-help.html')


def callback(request, twit_oath=None):

    context = {}
    
    oauth_token = request.GET.get('oauth_token')
    oauth_verifier = request.GET.get('oauth_verifier')
    oauth_denied = request.GET.get('denied')
    oauth_token_secret = request.session.get('oauth_token_secret')
    
    # print('oauth_token: ', oauth_token)
    # print('oauth_verifier: ', oauth_verifier)
    # print('oauth_denied: ', oauth_denied)
    # print('oauth_token_secret: ', oauth_token_secret)
    
    if oauth_token != request.session.get('oauth_token'):
        context['error_message'] = 'Returned oauth token does not match sent token.'   
        return render(request, 'img_app/error.html', context)

    if oauth_denied:
        context['error_message'] = 'the OAuth request was denied by this user'   
        return render(request, 'img_app/error.html', context)
    
    
    if not oauth_token or not oauth_verifier:
        context['error_message'] ="callback param(s) missing"
        return render(request, 'img_app/error.html', context)
    
    
    
    access_token, access_token_secret, error_message = callback_oath1handler(oauth_token, oauth_verifier, oauth_token_secret)
    request.session['access_token'] = access_token
    request.session['access_token_secret'] = access_token_secret
    


    if error_message:
        context['error_message'] = error_message
        return render(request, 'img_app/error.html', context)      
    
    
    return HttpResponseRedirect(reverse('img_app:index')) 
    

def authenticate(request):    
    context = {}
    
    authorization_url, oauth_token, oauth_token_secret, error_message = create_oath1_user_handler()
    if error_message:
        context['error_message'] = error_message
        return render(request, 'img_app/error.html', context)  
        
    
    context['authorization_url'] = authorization_url
    context['oauth_token'] = oauth_token

    request.session['oauth_token'] = oauth_token
    request.session['oauth_token_secret'] = oauth_token_secret
    
    return render(request, 'img_app/authenticate.html', context)
    

def sitemap(request):
    return render(request, 'img_app/sitemap.xml')