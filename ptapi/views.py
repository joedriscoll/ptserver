from django.shortcuts import render
from models import *
from django.http import HttpResponse as Ht
import json
import random
import string
import datetime
from django.views.decorators.csrf import csrf_exempt
def xauth(request):
	#if request.user.us_authenticated():
	return request.user
	
	#try:
		#type, token = request.META['HTTP_AUTHORIZATION"].split()
		#emailStr, passwordStr 

def hash(x):
	return x

####monday is 0
def getLast14Days():
	now = datetime.datetime.now()
	dates = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}
	i = 0
	while i <= 14:
		now = now - datetime.timedelta(days=1)
		dates[now.isoweekday()-1].append(now.strftime("%m/%d/%y"))
		i += 1
	return dates
	
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
			j = json.dumps({'success':1, 'assigned_pt':pair.assigned_pt.name})
		except:
			j = json.dumps({'success':1,'assigned_pt':'None'})
		return Ht(j,content_type = "application/json", status = 200)
	except:
		j = json.dumps({'success':2,'assigned_pt':'None'})
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
	print request
	try:
		user = User.objects.get(session_key = request.POST['session_key'])
		new_pain = Pain()
		new_pain.data = request.POST['data']
		new_pain.patient = user
		new_pain.save()
		j = json.dumps({'success':1})
		return Ht(j,content_type = "application/json", status = 200)
	except:
		j = json.dumps({'success':2})
		return Ht(j,content_type = "application/json", status = 200)



@csrf_exempt
def getPatientExercises(request):
	return Ht(j,content_type = "application/json", status = 200)
	if True:
		user = User.objects.get(session_key = request.POST['session_key'])
		#exercise_list = 
	today = datetime.date.isoweekday() - 1
	j = json.dumps({'success':1})
	return Ht(j,content_type = "application/json", status = 200)
	
	
@csrf_exempt
def updateExercise(request):
	j = json.dumps({'success':1})
	return Ht(j,content_type = "application/json", status = 200)
	'''
	if True:
		re
		user = User.objects.get(session_key = request.POST['session_key'])
		new_pain = Pain()
		new_pain.data = request.POST['data']
		new_pain.patient = user
		new_pain.save()
		j = json.dumps({'success':1})
		return Ht(j,content_type = "application/json", status = 200)
	else:
		j = json.dumps({'success':2})
		return Ht(j,content_type = "application/json", status = 200)
	'''

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
		
@csrf_exempt
def getPatients(request):
	try:
		user = User.objects.get(session_key = request.GET['session_key'])
		pair_list = Pair.objects.filter(assigned_pt = user)
		plist = [pair.patient.name for pair in pair_list]
		response = {'success':1, 'patient_list':plist}
		json_response = json.dumps(response)
		return Ht(json_response, content_type = "application/json")
	except:
		response = {'success':0, 'patient_list':[]}
		json_response = json.dumps(response)
		return Ht(json_response, content_type = "application/json")


def getExerciseResponse(patient):
	response = {}
	exercise_list = Exercise.objects.filter(patient = patient)
	dates = getLast14Days()
	all_exercises = []
	current_exercises = []
	for e in exercise_list:
		if e.name == '':
			e.name = 'aaa'
		if e.reps == '':
			e.reps = 'lll'
		e.save()
		assigned_days = json.loads(e.days_assigned)
		assigned_days = json.loads(assigned_days)
		all_exercises.append({'name':e.name, 'e_id':e.id, 'e_sets':e.reps, 'e_assigned_days':assigned_days})
		print e.lastFiveTimes
		if len(e.lastFiveTimes) > 1:
			last5 = json.loads(e.lastFiveTimes)
		else:
			last5 = []
		print last5
		print assigned_days
		for d in range(len(assigned_days)):
			if assigned_days[d]  == 1:
				for alld in dates[d]:
					found = False
					for x in last5:
						if alld == x['date']:
							found = True
							current_exercises.append({'name':e.name, 'e_id':e.id, 'e_sets':e.reps, 'e_assigned_days':assigned_days, 'e_date': alld, "e_completion":int(x['completion'])})
					if found == False:
						current_exercises.append({'name':e.name, 'e_id':e.id, 'e_sets':e.reps, 'e_date': alld, 'e_assigned_days':assigned_days,"e_completion":0})
	response = {"success":1, "all_exercises":all_exercises, "current_exercises":current_exercises}
	return response


@csrf_exempt
def postExerciseInstance(request):
	user = User.objects.get(session_key = request.POST['session_key'])
	exercise = Exercise.objects.get(id = request.POST['exercise_id'])
	print exercise.lastFiveTimes
	if exercise.lastFiveTimes == '':
		dates = []
	else:
		dates = json.loads(exercise.lastFiveTimes)
	new_date = request.POST['exercise_date']
	found = False
	for x in dates:
		if x['date'] == new_date:
			x['completion'] = request.POST['exercise_completion']
			found = True
	print 'went through loops'
	if found == False:
		dates.append({'date':new_date, 'completion': request.POST['exercise_completion']})
		print 'abbbend'
	if len(dates) > 24:
		dates.pop(-1)
	print 'about to save'
	exercise.lastFiveTimes = json.dumps(dates)
	exercise.save()
	exercise_list = Exercise.objects.filter(patient = user)
	now = datetime.datetime.now()
	now_num = now.isoweekday() - 1 
	now_date = now.strftime("%m/%d/%y")
	tomorrow = now + datetime.timedelta(days = 1)
	tomorrow_num = tomorrow.isoweekday() - 1
	tomorrow_date = tomorrow.strftime("%m/%d/%y")
	yesterday = now + datetime.timedelta(days = -1)
	yesterday_num = yesterday.isoweekday() - 1
	yesterday_date = yesterday.strftime("%m/%d/%y")
	td = {"exercise_name":[], "exercise_id": [], "reps":[],"date":now_date}
	rd = {"exercise_name":[], "exercise_id": [], "reps":[],"date":tomorrow_date}
	yd = {"exercise_name":[], "exercise_id": [], "reps":[],"date":yesterday_date}
	for e in exercise_list:
		assigned_days = json.loads(json.loads(e.days_assigned))
		
		if int(assigned_days[now_num]) > 0:
			print 'it was found today'
			td["exercise_name"].append(e.name)
			td["exercise_id"].append(e.id)
			td["reps"].append(e.reps)
		if int(assigned_days[tomorrow_num]) > 0:
			rd["exercise_name"].append(e.name)
			rd["exercise_id"].append(e.id)
			rd["reps"].append(e.reps)
		if int(assigned_days[yesterday_num]) > 0:
			yd["exercise_name"].append(e.name)
			yd["exercise_id"].append(e.id)
			yd["reps"].append(e.reps)
	print 'response'
	response = {"success":1, "td":td, "rd":rd, "yd":yd}
	json_response = json.dumps(response)
	return Ht(json_response, content_type = "applicaiton/json")
	
@csrf_exempt
def getExercisesForPatient(request):
	now = datetime.datetime.now()
	now_num = now.isoweekday() - 1 
	now_date = now.strftime("%m/%d/%y")
	tomorrow = now + datetime.timedelta(days = 1)
	tomorrow_num = tomorrow.isoweekday() - 1
	tomorrow_date = tomorrow.strftime("%m/%d/%y")
	yesterday = now + datetime.timedelta(days = -1)
	yesterday_num = yesterday.isoweekday() - 1
	yesterday_date = yesterday.strftime("%m/%d/%y")
	print now_num
	print tomorrow_num
	print yesterday_num
	if True:
		user = User.objects.get(session_key = request.GET['session_key'])
		exercise_list = Exercise.objects.filter(patient = user)
		td = {"exercise_name":[], "exercise_id": [], "reps":[],"date":now_date}
		rd = {"exercise_name":[], "exercise_id": [], "reps":[],"date":tomorrow_date}
		yd = {"exercise_name":[], "exercise_id": [], "reps":[],"date":yesterday_date}
		for e in exercise_list:
			assigned_days = json.loads(json.loads(e.days_assigned))
			print e.name
			print assigned_days
			print assigned_days[now_num]
			print 'hihihi'
			if int(assigned_days[now_num]) > 0:
				print 'it was found today'
				td["exercise_name"].append(e.name)
				td["exercise_id"].append(e.id)
				td["reps"].append(e.reps)
			if int(assigned_days[tomorrow_num]) > 0:
				rd["exercise_name"].append(e.name)
				rd["exercise_id"].append(e.id)
				rd["reps"].append(e.reps)
			if int(assigned_days[yesterday_num]) > 0:
				yd["exercise_name"].append(e.name)
				yd["exercise_id"].append(e.id)
				yd["reps"].append(e.reps)
		print td
		print rd
		print yd
		response = {"success":1, "td":td, "rd":rd, "yd":yd}
		json_response = json.dumps(response)
		return Ht(json_response, content_type = "applicaiton/json")
		
@csrf_exempt
def getPatientsExerciseData(request):
#get the pair
	print request
	print request.POST['patient_username'] + 'hihi'
	patient = User.objects.get(name = request.POST['patient_username'])
	response = {"success":1, "all_exercises":[{"name":"hug","e_id":0, "e_sets":"there was a time", "e_assigned_days":[0,0,1,0,0,0,0]}], "current_exercises":[{"name":"kiss","e_id":0,"e_date":"8/11/14","e_completion":0}]}
	response = getExerciseResponse(patient)
	json_response = json.dumps(response,ensure_ascii = True)
	print json_response
	return Ht(json_response, content_type = "application/json")
	
@csrf_exempt
def editExerciseData(request):
#get the pair
	patient = User.objects.get(name = request.POST['patient_username'])
	exercise = Exercise.objects.get(id = request.POST['e_id'])
	exercise.name = request.POST['name']
	exercise.reps = request.POST['sets']
	exercise.days_assigned = json.dumps(request.POST['assigned_days'])
	exercise.save()
	response = getExerciseResponse(patient)
	#response = {"success":1, "all_exercises":[{"name":"hug","e_id":0, "e_sets":"there was a time", "e_assigned_days":[0,0,1,0,0,0,0]}], "current_exercises":[{"name":"kiss","e_id":0,"e_date":"8/11/14","e_completion":0}]}
	json_response = json.dumps(response)
	return Ht(json_response, content_type = "application/json")



		
		
@csrf_exempt
def addNewExercise(request):
	if True:
		user = User.objects.get(session_key = request.POST['session_key'])
		patient = User.objects.get(name = request.POST['patient_username'])
		pair = Pair.objects.get(patient = patient)
		if pair.assigned_pt == user:
			new_exercise = Exercise()
			new_exercise.name = request.POST['name']
			new_exercise.days_assigned = json.dumps(request.POST['assinged_days'])
			new_exercise.reps = request.POST['sets']
			new_exercise.patient = patient
			new_exercise.save()
	response = {"success":1, "all_exercises":[{"name":"hug","e_id":0, "e_sets":"there was a time", "e_assigned_days":[0,0,1,0,0,0,0]}], "current_exercises":[{"name":"kiss","e_id":0,"e_date":"8/11/14","e_completion":0}]}
	json_response = json.dumps(response)
	return Ht(json_response, content_type = "application/json")
	
	
@csrf_exempt
def getActivity(request):
	if True:
		user = User.objects.get(session_key = request.GET['session_key'])
		patient = User.objects.get(name = request.GET['patient_username'])
		pair = Pair.objects.get(patient = patient)
		if pair.assigned_pt != user:
			response = {'success':0}
			json_response = json.dumps(response)
			return Ht(json_response, content_type = "application/json")
		else:
			response = {'success':1, 'graphs':[{'name':'Monday', 'data':{'activity':[100 for x in range(12)], 'pain':[1,2,0,0,0,0,2,0,0,0,0,0]}}, {'name':'Tuesday', 'data':{'activity':[100 for x in range(12)], 'pain':[1,2,0,0,0,0,2,0,0,0,0,0]}}]}
			json_response = json.dumps(response)
			return Ht(json_response, content_type = "application/json")
	else:
		return Ht("Invalid Request", status = 400)
			
		'''
		time_delta = datetime.datetime.now() - datetime.timedelta(days = 14)
		act_list = Activity.models.filter(patient = person, time_lt = time_delta)
		response = [{'time':act.time, 'data':act.data, 'type': act.type} for act in act_list]
		json_response = json.loads(response)
		return Ht(json_response, content_type = "application/json")
	except:
		return Ht("Invalid Requset", status = 400)
		'''
		
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
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	