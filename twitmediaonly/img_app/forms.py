from django import forms

class ArtistForm(forms.Form):
    artist_name = forms.CharField(label = "Artist name", max_length= 100)
    
    
    