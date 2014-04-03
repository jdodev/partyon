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