from django import forms
from django.forms import ModelForm
from webapp.models import *
from datetime import datetime
from django.contrib.auth.models import User

class PhotoPostForm(ModelForm):
	class Meta:
		model = PhotoPost

class SongPostForm(ModelForm):
	class Meta:
		model = SongPost

class AddPlaceForm(ModelForm):
	class Meta:
		model = Place

class SignUpForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name']
		widgets = {
		'password' : forms.PasswordInput(),
		}

class UserProfileForm(forms.Form):
	UserProfilePhoto = models.ImageField(upload_to='UserProfilePhotos', default='UserProfilePhotos/partyon_img_prof_def_jpg.jpg')
	UserProfileID = models.IntegerField(help_text='UserProfile ID', verbose_name=u'UserProfile ID')

class fsqCityNameForm(forms.Form):
	CityName = forms.CharField(max_length=50, help_text='City Name')
	fsqToken = forms.CharField(max_length=250, help_text='Foursquare Token')