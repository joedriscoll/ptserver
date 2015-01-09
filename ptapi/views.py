from django.shortcuts import render
from models import *
from django.http import HttpResponse as Ht
import json
import random
import string
from django.views.decorators.csrf import csrf_exempt
def xauth(request):
	#if request.user.us_authenticated():
	return request.user
	
	#try:
		#type, token = request.META['HTTP_AUTHORIZATION"].split()
		#emailStr, passwordStr 

def hash(x):
	return x

def index(request):
	return Ht("You are at the PT Assistant Server!")
# Create your views here.
@csrf_exempt
def login(request):
	#print request.POST['username']
	try:
		user = User.objects.get(name = request.POST['username'])
		if user.password_hash == hash(request.POST['password']):
			session_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(1000))+user.name
			user.session_key = session_key
			user.save()
			j = json.dumps({'success':1,'session_key':session_key})
			return Ht(j,content_type = "application/json")
		else:
			j = json.dumps({'success':2,'UserName':user.name})
			return Ht(j,content_type = "application/json")
	except:
		print 'hihihih'
		return  Ht("Invalid Request", status = 400)

@csrf_exempt
def register(request):
	try:
		new_user = User()
		new_user.name = request.POST['username']
		new_user.email = request.POST['email']
		new_user.password_hash = hash(request.POST['password'])
		if request.POST['type'] == 'pt':
			new_user.is_pt = True
		new_user.save()
		j = json.dumps({'success':1})
		return Ht(j, content_type = "application/json", status = 200)
	except:
		return Ht("Invalid Request", status = 400)
	
@csrf_exempt
def getSettings(request):
	try:
		user = User.objects.get(session_key = request.GET['session_key'])
		print 'aaaaaaa'
		try:
			pair = Pair.objects.get(patient = user)
			j = json.dumps({'assigned_pt':pair.assigned_pt.name})
		except:
			j = json.dumps({'assigned_pt':'None'})
		return Ht(j,content_type = "application/json", status = 200)
	except:
		j = json.dumps({'assigned_pt':'None'})
		return Ht(j,content_type = "application/json", status = 200)
		
@csrf_exempt
def addPair(request):
	if True:
		user = User.objects.get(session_key = request.POST['session_key'])
		try:
			pt = User.objects.get(name = request.POST['pt_username'])
			if pt.is_pt != True:
				j = json.dumps({'success':2})
				return Ht(j,content_type = "application/json", status = 200)
		except:
			j = json.dumps({'success':2})
			return Ht(j,content_type = "application/json", status = 200)
		try:
			pairlist = Pair.objects.filter(patient = user)
			pair.delete()
		except:
			pass
		new_pair = Pair()
		new_pair.patient = user
		new_pair.assigned_pt = pt
		new_pair.save()
		j = json.dumps({'success':1})
		return Ht(j,content_type = "application/json", status = 200)
		

@csrf_exempt
def logPain(request):
	return Ht(json.dumps({'success':1,}),content_type = "application/json")
	user = xauth(request)
	if user == None:
		return getAuth(request)
	try:	
		new_pain = Pain()
		new_pain.data = request.POST['data']
		new_pain.patient = user
		new_pain.save()
	except:
		return Ht("Invalid Request", status = 400)
	return Ht('saved',content_type = "application/json")

def addActivity(request):
	user = xauth(request)
	if user == None:
		return getAuth(request)
	try:
		new_act = Activity()
		new_act.type = request.POST['type']
		new_act.data = request.POST['data']
		new_act.patient = user
		new_act.save()
	except:
		return Ht("Invalid Requst", status = 400)
	return Ht('saved', content_type = "application/json")
	
def getPain(request):
	user = xauth(request)
	if user == None:
		return getAuth(request)
	try:
		person_id = request.GET['id']
		person = User.models.get(id = person_id)
		#check to make sure the patient is assigned this pt
		joined = Pair.models.get(patient = person)
		if joined.assigned_pt != user:
			return Ht('not assigned patient', status = 400)
		time_delta = datetime.datetime.now() - datetime.timedelta(days = 14)
		pain_list = Pain.models.filter(patient = person, time_lt = time_delta)
		response = [{'time': pain.time, 'data': pain.data} for pain in pain_list]
		json_response = json.loads(response)
		return Ht(json_response, content_type = "application/json")
	except:
		return Ht("Invalid Request", status = 400)

def getPatients(request):
	user = xauth(request)
	if user == None:
		return getAuth(request)
	try:
		pair_list = Pait.models.get(assigned_pt = user)
		response = [{'name': pair.patient.name, 'id': pair.patient.id} for pair in pair_list]
		json_response = json.loads(response)
		return Ht(json_response, content_type = "application/json")
	except:
		return Ht("Invalid Requset", status = 400)

def getActivity(requset):
	user = xauth(request)
	if user == None:
		return getAuth(request)
	try:
		person_id = requset.GET('id')
		person = User.models.get(id = person_id)
		
		joined = Pair.models.get(patient = person)
		if joined.assigned_pt != user:
			return Ht('not assigned patient', status = 400)
		time_delta = datetime.datetime.now() - datetime.timedelta(days = 14)
		act_list = Activity.models.filter(patient = person, time_lt = time_delta)
		response = [{'time':act.time, 'data':act.data, 'type': act.type} for act in act_list]
		json_response = json.loads(response)
		return Ht(json_response, content_type = "application/json")
	except:
		return Ht("Invalid Requset", status = 400)
		
def addPossiblePair(requset):
	user = xauth(request)
	if user == None:
		return getAuth(requset)			 
	try:
		person_id = request.POST('id')
		person = User.models.get(id = person_id)
		new_pp = PossiblePair()
		new_pp.assinged_pt = user
		new_pp.patient = person
		new_pp.save()
		return Ht('good', content_type = "application/json")
	except:
		return Ht("Invalid Request", status = 400)

def confirmPossiblePair(request):
	user = xauth(request)
	if user == None:
		return getAuth(request)
	try:
		pp_id = requset.POST('pp_id')
		pp = PossiblePair.models.get(id = pp_id)
		if pp.patient != user:
		
			return Ht('Invalid Requset', status = 400)
		new_p = Pair()
		new_p.assigned_pt = pp.assigned_pt
		new_p.patient = pp.patient
		new_p.save()
		pp.delet()
		return Ht('good', content_type = "application/json")
	except:
		return Ht('Invalid Request', status = 400)
		
def getPossiblePair(request):
	user = xauth(requset)
	if user == None:
		return getAuth(request)
	try:
		pp_list = PossiblePair.models.filter(patient = user)
		response = [{'pt':pp.assigned_pt, 'patient': pp.patient} for pp in pp_list]
		json_resposne = json.loads(response)
		return Ht(json_resposne, content_type = "application/json")
	except:
		return Ht('Invalid Response', status = 400)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	