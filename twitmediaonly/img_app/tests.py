from django.test import TestCase
from django.test import Client
# Create your tests here.

class ArtistSearchBarTest(TestCase):
  
    
    def do_search(self, search):
        response = self.client.post('/post_redirect/', {'artist_name': search}, follow=True)
        expected_url = '/name/' + search + '/'
        
        self.assertEqual(response.request['PATH_INFO'], expected_url)
        self.assertEqual(response.status_code, 200)        
        return response
        
    def test_good_search(self):
        search = 'binka_jar'
        response = self.do_search(search)
        self.assertIn('page_obj', response.context)
        
    
    def test_bad_search(self):
        search = 'binka_jarchuckleface281'
        response = self.do_search(search)
        self.assertNotIn('page_obj', response.context)
        
    def test_real_user_no_media(self):
        search='chucklefuck'
        response = self.do_search(search)
        self.assertNotIn('page_obj', response.context)
    
    
    def test_post_search_from_different_artist(self):
        response = self.client.get('/i/1502984775748915202?order=top')
        self.assertIn('tweet_objs', response.context)
        self.assertEqual(response.context['previous_tweet'], '')
        self.assertEqual(response.context['next_tweet'], '')
        #self.assertEqual(response.context['current_params'], '?order=top')
        
        
    def test_link(self):
        # response = self.client.get('/i/1502984775748915202?order=top')
        response = self.client.get('/i/1361285649937141761')
        self.assertIn('tweet_objs', response.context)
        self.assertEqual(response.context['previous_tweet'], '')
        self.assertEqual(response.context['next_tweet'], '')
        #self.assertEqual(response.context['current_params'], '?order=top')
        
    
    
