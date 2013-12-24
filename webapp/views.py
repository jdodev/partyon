# -*- encoding: utf-8 -*-
from datetime import datetime
from django.core import serializers
from django.db.models import Count, Max, Sum, Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from models import *

def index(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/home/')
	else:
		#loginForm = AuthenticationForm()
		#return render(request, 'login.html', {'loginForm' : loginForm})
		return (HttpResponseRedirect('/admin/'))

@login_required(login_url='/')
def home(request):
	return render(request, 'home.html')

@login_required(login_url='/')
def datahome(request):
	if request.is_ajax():
		resPlaces = Place.objects.all()
		return render(request, 'datahome.html', {'TPlaces' : resPlaces})

@login_required(login_url='/')
def datatrends(request):
	if request.is_ajax():
		resPlaces = Place.objects.all()
		return render(request, 'datatrends.html', {'TPlaces' : resPlaces})

@login_required(login_url='/')
def dataactivity(request):
	if request.is_ajax():
		resUserActivity = PhotoPost.objects.all().order_by('-PhotoPostID')
		return render(request, 'dataactivity.html', {'TUserActivity' : resUserActivity})

@login_required(login_url='/')
def dataheydj(request):
	if request.is_ajax():
		resHeyDj = SongPost.objects.all().order_by('-SongPostID')
		return render(request, 'dataheydj.html', {'THeyDj' : resHeyDj})

@login_required(login_url='/')
def postphoto(request):
	return render(request, 'postphoto.html')

@login_required(login_url='/')
def login(request):
	return render(request, 'login.html')