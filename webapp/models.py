#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Place(models.Model):
	PlaceID = models.AutoField(primary_key=True)
	PlaceName = models.CharField(max_length=50, help_text='Place Name', verbose_name=u'Name')
	PlaceLat = models.CharField(max_length=25, help_text='Place Latitude', verbose_name=u'Latitude')
	PlaceLong = models.CharField(max_length=25, help_text='Place Longitude', verbose_name=u'Longitude')
	PlaceLogo = models.ImageField(upload_to='PlaceLogos', verbose_name=u'Logo')

	def __unicode__(self):
		return self.PlaceName

class PhotoPost(models.Model):
	PhotoPostID = models.AutoField(primary_key=True)
	PhotoPostDateTime = models.DateTimeField(auto_now_add=True, help_text='Date of post', verbose_name=u'Date')
	PhotoPost_PlaceID = models.ForeignKey(Place)
	PhotoPostPhoto = models.ImageField(upload_to='PhotoPosts')
	PhotoPost_User = models.ForeignKey(User)
	PhotoPost_Lat = models.CharField(max_length=25, help_text='Post Latitude', verbose_name=u'Latitude')
	PhotoPostLong = models.CharField(max_length=25, help_text='Post Longitude', verbose_name=u'Logintude')
	PhotoPostDescription = models.CharField(max_length=140, help_text='Post Description', verbose_name=u'Description', blank=True, null=True)

	def __unicode__(self):
		return self.PhotoPostDescription

class SongPost(models.Model):
	SongPostID = models.AutoField(primary_key=True)
	SongPostDateTime = models.DateTimeField(auto_now_add=True, help_text='Date of Song', verbose_name=u'Date')
	SongPost_PlaceID = models.ForeignKey(Place)
	SongPostName = models.CharField(max_length=50, help_text='Song Name', verbose_name=u'Name')
	SongPost_User = models.ForeignKey(User)
	SongPostLat = models.CharField(max_length=25, help_text='Song Latitude', verbose_name=u'Latitude')
	SongPostLong = models.CharField(max_length=25, help_text='Song Longitude', verbose_name=u'Longitude')
	SongPostQuote = models.CharField(max_length=140, help_text='Song Quote', verbose_name=u'Quote', blank=True, null=True)

	def __unicode__(self):
		return self.SongPostName

class SongPoint(models.Model):
	SongPointID = models.AutoField(primary_key=True)
	SongPoint_SongPostID = models.ForeignKey(SongPost)
	SongPoint_User = models.ForeignKey(User)

	def __unicode__(self):
		return str(self.SongPointID)

class PhotoPoint(models.Model):
	PhotoPointID = models.AutoField(primary_key=True)
	PhotoPoint_PhotoPostID = models.ForeignKey(PhotoPost)
	PhotoPoint_User = models.ForeignKey(User)

	def __unicode__(self):
		return self.PhotoPointID

class AppInfo(models.Model):
	AppInfoID = models.AutoField(primary_key=True)
	AboutUs = models.TextField(help_text='About Us', verbose_name=u'AboutUs')
	TermsOfUse = models.TextField(help_text='Terms of Use', verbose_name=u'TermsOfUse')
	Privacy = models.TextField(help_text='Privacy', verbose_name=u'Privacy')
	Help = models.TextField(help_text='Help Information', verbose_name=u'Help')
	EmailContact = models.EmailField(max_length=75, help_text='Contact Email', verbose_name=u'Contact')

	def __unicode__(self):
		return self.AppInfoID

class UserProfile(models.Model):
	UserProfileID = models.AutoField(primary_key=True)
	UserProfile_User = models.ForeignKey(User)
	UserProfilePhoto = models.ImageField(upload_to='UserProfilePhotos', blank=True, null=True)
	UserProfileMailVerified = models.BooleanField(help_text='User Mail Verified', verbose_name=u'Mail Verified')

	def __unicode__(self):
		return self.UserProfile_User.username

class Follow(models.Model):
	FollowID = models.AutoField(primary_key=True)
	FollowOwner_User = models.ForeignKey(User, related_name='OwnerUser')
	Follow_User = models.ForeignKey(User, related_name='FollowUser')

	def __unicode__(self):
		return self.FollowID