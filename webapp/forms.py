from django import forms
from django.forms import ModelForm
from webapp.models import *
from datetime import datetime

class PhotoPostForm(ModelForm):
	class Meta:
		model = PhotoPost

class SongPostForm(ModelForm):
	class Meta:
		model = SongPost