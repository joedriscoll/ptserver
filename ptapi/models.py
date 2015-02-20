from django.db import models


class User(models.Model):
	is_pt = models.BooleanField(default = False)
	password_hash = models.CharField(max_length = 200)
	name = models.CharField(max_length = 100, unique = True)
	email = models.CharField(max_length = 100)
	session_key = models.CharField(max_length = 2000, null = True, blank = True)
	session_ip = models.GenericIPAddressField(null = True, blank = True)

class Pair(models.Model):
	assigned_pt = models.ForeignKey(User, related_name = 'assinged_pt')
	patient = models.ForeignKey(User, primary_key = True)
	
class Pain(models.Model):
	patient = models.ForeignKey(User)
	time = models.CharField(max_length = 300, null = True, blank = True)
	hour = models.IntegerField(null = True, blank = True)
	data = models.CharField(max_length = 300)

class Activity(models.Model):
	patient = models.ForeignKey(User)
	time = models.CharField(max_length = 100, null = True, blank = True)
	data = models.CharField(max_length = 100)
	type = models.CharField(max_length = 100)
	hour = models.IntegerField(null = True, blank = True)
	unique_together = (('hour','time','patient'))
	
class PossiblePair(models.Model):
	assigned_pt = models.ForeignKey(User, related_name = 'assigned_pt')
	patient = models.ForeignKey(User)
	
class Exercise(models.Model):
	patient = models.ForeignKey(User)
	days_assigned = models.CharField(max_length = 20)
	name = models.CharField(max_length = 100)
	reps = models.CharField(max_length = 100, null = True, blank = True)
	lastFiveTimes = models.CharField(max_length = 400)
	first_day = models.DateTimeField(auto_now = True)

class Achievement(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 400)
	
class UserAchievement(models.Model):
	user = models.ForeignKey(User)
	achievement = models.ForeignKey(Achievement)
	unique_together = (('user','achievement'),)

	
	
	
# Create your models here.

