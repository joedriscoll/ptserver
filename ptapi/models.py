from django.db import models


class User(models.Model):
	is_pt = models.BooleanField(default = False)
	password_hash = models.CharField(max_length = 200)
	name = models.CharField(max_length = 100, unique = True)
	email = models.CharField(max_length = 100)
	session_key = models.CharField(max_length = 2000, null = True, blank = True)

class Pair(models.Model):
	assigned_pt = models.ForeignKey(User, related_name = 'assinged_pt')
	patient = models.ForeignKey(User, primary_key = True)
	
class Pain(models.Model):
	patient = models.ForeignKey(User)
	time = models.DateTimeField(auto_now = True)
	data = models.CharField(max_length = 300)

class Activity(models.Model):
	patient = models.ForeignKey(User)
	time = models.DateTimeField(auto_now = True)
	data = models.CharField(max_length = 100)
	type = models.CharField(max_length = 100)
	
class PossiblePair(models.Model):
	assigned_pt = models.ForeignKey(User, related_name = 'assigned_pt')
	patient = models.ForeignKey(User)
	
class Exercise(models.Model):
	patient = models.ForeignKey(User)
	days_assigned = models.CharField(max_length = 7)
	name = models.CharField(max_length = 100)
	reps = models.CharField(max_length = 100, null = True, blank = True)
	lastFiveTimes = models.CharField(max_length = 400)
	first_day = models.DateTimeField(auto_now = True)


	
	
	
# Create your models here.

