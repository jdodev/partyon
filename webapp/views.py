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
from webapp.forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
import json

def index(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/home/')
	else:
		loginForm = AuthenticationForm()
		return render(request, 'login.html', {'loginForm' : loginForm})
		#return (HttpResponseRedirect('/admin/'))

def loginpartyon(request):
	loginForm = AuthenticationForm()
	if request.is_ajax():
		if request.method == 'POST':
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				login(request, acceso)
				respuesta = {'codigo': 1, 'msg': 'Welcome to partyon'}
				return HttpResponse(json.dumps(respuesta))
				#return HttpResponseRedirect('/')
			else:
				respuesta = {'codigo': 2, 'msg': 'You have entered an incorrect email or password.'}
				return HttpResponse(json.dumps(respuesta))
				#return render(request, 'login.html', {'loginForm' : loginForm})
		else:
			return render(request, 'login.html', {'loginForm' : loginForm})
	else:
		return render(request, 'login.html', {'loginForm' : loginForm})

@login_required(login_url='/')
def logoutpatyon(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/')
def savephotopost(request):
	if request.method == 'POST':
		formPhotoPost = PhotoPostForm(request.POST, request.FILES)
		if formPhotoPost.is_valid():
			u = formPhotoPost.save(commit=False)
			u.PhotoPostDateTime = datetime.now()
			u.save()
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/novalid/')
	else:
		return HttpResponseRedirect('/nopost/')

def novalido(request):
	formPhotoPost = PhotoPostForm()
	return render(request, 'novalidod.html', {'form' : formPhotoPost})

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
	resNearPlaces = Place.objects.all()
	return render(request, 'postphoto.html', {'NearPlaces' : resNearPlaces})

@login_required(login_url='/')
def settings(request):
	return render(request, 'settings.html')

@login_required(login_url='/')
def help(request):
	return render(request, 'help.html')