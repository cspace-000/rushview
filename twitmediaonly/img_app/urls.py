from django.urls import path
from . import views


app_name = 'img_app'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('name/<str:artist_name>/', views.artist, name = 'artist'),
    #path('name/<int:artist_name>', views.artist, name = 'artist'),
    path('name/<str:artist_name>/page/<int:page_num>', views.a_page, name = 'a_page'),
    #path('name/<str:artist_name>/ajax/paginate/', views.paginate, name = 'paginate'),
    

    path('search/<str:query>/', views.search, name='search'),
    path('search/<str:query>/page/<int:page_num>', views.q_page, name = 'q_page'),

    
    path('post_redirect/', views.post_redirect, name = 'post_redirect'),

    
    
    path('i/<int:tweet_id>', views.post, name='post'),
    path('about/', views.about, name='about'),
   # path('about/(?[0-9][a-z])', views.about, name='about'),
    
    
    path('search-help/', views.search_help, name='search-help'),
    path('callback', views.callback, name='callback'),
    path('callback/', views.callback, name='callback'),
    path('authenticate/(?[0-9][a-z])', views.authenticate, name = 'authenticate'),
    path('authenticate/', views.authenticate, name = 'authenticate'),
    path('sitemap/', views.sitemap, name='sitemap'),
   # path('authenticate/', views.authenticate, name = 'authenticate'),

    # path('test_page/', views.test_page, name = 'test_page'),
    # path('test_ajax/', views.test_ajax, name = 'test_ajax'),
    
]