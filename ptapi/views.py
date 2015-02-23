from django.shortcuts import render
from models import *
from django.http import HttpResponse as Ht
import json
import random
import string
import datetime
from django.views.decorators.csrf import csrf_exempt
from ipware.ip import get_ip
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


def get3Days():
	now = datetime.datetime.now()
	now = now + datetime.timedelta(days = 2)
	dates = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}
	i = 0
	while i < 3:
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
	if True:
		user = User.objects.get(name = request.POST['username'])
		if user.password_hash == hash(request.POST['password']):
			session_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(1000))+user.name
			user.session_key = session_key
			#ip = get_ip(request)
			#if ip is not None:
			#	user.session_ip = request.META['HTTP_X_FORWARDED_FOR']
			#else:
			#	user.session_ip = "0.0.0.0.0.0"
			user.save()
			j = json.dumps({'success':1,'session_key':session_key})
			return Ht(j,content_type = "application/json")
		else:
			j = json.dumps({'success':2,'UserName':user.name})
			return Ht(j,content_type = "application/json")
	else:
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
	try:
		user = User.objects.get(session_key = request.POST['session_key'])
		try:
			pain = Pain.objects.get(patient = user, hour = request.POST['hour'], time = request.POST['time'])
			pain.data = request.POST['data']
			pain.save()
		except:
			new_pain = Pain()
			new_pain.data = request.POST['data']
			new_pain.patient = user
			new_pain.hour = int(request.POST['hour'])
			new_pain.time = request.POST['time']
			new_pain.save()
		j = json.dumps({'success':1})
		return Ht(j,content_type = "application/json", status = 200)
	except:
		j = json.dumps({'success':2})
		return Ht(j,content_type = "application/json", status = 200)
	

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
						current_exercises = sorted(current_exercises, key = lambda x: x['e_date'])[::-1]
	response = {"success":1, "all_exercises":all_exercises, "current_exercises":current_exercises}
	return response

def get3DayExerciseResponse(patient):
	response = {}
	exercise_list = Exercise.objects.filter(patient = patient)
	print exercise_list
	dates = get3Days()
	print dates
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
						current_exercises = sorted(current_exercises, key = lambda x: x['e_date'])[::-1]
	response = {"success":1, "all_exercises":all_exercises, "current_exercises":current_exercises}
	print response['current_exercises']
	return response
	
@csrf_exempt
def postExerciseInstance(request):
	user = User.objects.get(session_key = request.POST['session_key'])
	exercise = Exercise.objects.get(id = request.POST['exercise_id'])
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
	if found == False:
		dates.append({'date':new_date, 'completion': request.POST['exercise_completion']})
	if len(dates) > 24:
		dates.pop(-1)
	exercise.lastFiveTimes = json.dumps(dates)
	exercise.save()
	request.GET = request.POST
	return getExercisesForPatient(request)
	'''
	exercise_list = Exercise.objects.filter(patient = user)
	now = datetime.datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
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
	'''
	
@csrf_exempt
def oldgetExercisesForPatient(request):
	now = datetime.datetime.strptime(request.GET['date'], "%Y-%m-%d").date()
	print now
	now_num = now.isoweekday() - 1 
	now_date = now.strftime("%m/%d/%y")
	tomorrow = now + datetime.timedelta(days = 1)
	tomorrow_num = tomorrow.isoweekday() - 1
	tomorrow_date = tomorrow.strftime("%m/%d/%y")
	yesterday = now + datetime.timedelta(days = -1)
	yesterday_num = yesterday.isoweekday() - 1
	yesterday_date = yesterday.strftime("%m/%d/%y")
	if True:
		user = User.objects.get(session_key = request.GET['session_key'])
		exercise_list = Exercise.objects.filter(patient = user)
		td = {"exercise_name":[], "exercise_id": [], "reps":[],"date":now_date}
		rd = {"exercise_name":[], "exercise_id": [], "reps":[],"date":tomorrow_date}
		yd = {"exercise_name":[], "exercise_id": [], "reps":[],"date":yesterday_date}
		for e in exercise_list:
			assigned_days = json.loads(json.loads(e.days_assigned))
			if int(assigned_days[now_num]) > 0:
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
		response = {"success":1, "td":td, "rd":rd, "yd":yd}
		json_response = json.dumps(response)
		return Ht(json_response, content_type = "applicaiton/json")

@csrf_exempt
def getExercisesForPatient(request):
	if True:
		print 'today'
		today = datetime.datetime.now()
		tomorrow = today + datetime.timedelta(days = 1)
		yesterday = today - datetime.timedelta(days = 1)
		user = User.objects.get(session_key = request.GET['session_key'])
		r = get3DayExerciseResponse(user)
		current = r['current_exercises']
		exercise_list = Exercise.objects.filter(patient = user)
		td = {"exercise_name":[], "exercise_id": [], "reps":[],"date":today.strftime('%m/%d/%y'), "completion":[]}
		rd = {"exercise_name":[], "exercise_id": [], "reps":[],"date":tomorrow.strftime('%m/%d/%y'),"completion":[]}
		yd = {"exercise_name":[], "exercise_id": [], "reps":[],"date":yesterday.strftime('%m/%d/%y'),"completion":[]}
		print 'setup'
		for e in current:
			if e['e_date'] == today.strftime('%m/%d/%y'):
				td["exercise_name"].append(e['name'])
				td["exercise_id"].append(e['e_id'])
				td["reps"].append(e['e_sets'])
				td["completion"].append(e['e_completion'])
			if e['e_date'] == tomorrow.strftime('%m/%d/%y'):
				rd["exercise_name"].append(e['name'])
				rd["exercise_id"].append(e['e_id'])
				rd["reps"].append(e['e_sets'])
				rd["completion"].append(e['e_completion'])
			if e['e_date'] == yesterday.strftime('%m/%d/%y'):
				yd["exercise_name"].append(e['name'])
				yd["exercise_id"].append(e['e_id'])
				yd["reps"].append(e['e_sets'])
				yd["completion"].append(e['e_completion'])
		response = {"success":1, "td":td, "rd":rd, "yd":yd}
		json_response = json.dumps(response)
		return Ht(json_response, content_type = "applicaiton/json")

		
@csrf_exempt
def getPatientsExerciseData(request):
#get the pair
	patient = User.objects.get(name = request.GET['patient_username'])
	response = getExerciseResponse(patient)
	json_response = json.dumps(response,ensure_ascii = True)
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
def getAchievements(request):
	if True:
		user = User.objects.get(session_key = request.GET['session_key'])
		response = {'success':1, "nameToD":{'first':"this is the first thing", 'second':"This is the second thing"}, "complete":['first','second']}
		json_response = json.dumps(response)
		return Ht(json_response, content_type = "application/json")
		
		
@csrf_exempt
def addNewExercise(request):
	if True:
		user = User.objects.get(session_key = request.POST['session_key'])
		patient = User.objects.get(name = request.POST['patient_username'])
		pair = Pair.objects.get(patient = patient)
		print 'gotit'
		print request
		if pair.assigned_pt == user:
			print 'allowed'
			new_exercise = Exercise()
			print 'exercise'
			new_exercise.name = request.POST['name']
			print 'name'
			print request.POST['assigned_days']
			new_exercise.days_assigned = json.dumps(request.POST['assigned_days'])
			print 'days'
			new_exercise.reps = request.POST['sets']
			new_exercise.patient = patient
			new_exercise.save()
			response = getExerciseResponse(patient)
			json_response = json.dumps(response,ensure_ascii = True)
			return Ht(json_response, content_type = "application/json")
		else:
			return Ht(json_dumps({"success":2}), content_type = "application/json")
	
@csrf_exempt
def addSteps(request):
	if True:
		user = User.objects.get(session_key = request.POST['session_key'])
		#user = User.objects.get(name = "joe")
		for step in request.POST['data']:
			try:
				act = Activity.objects.get(time = step['date'], hour = int(step['hour']), type = 'steps')
				if act.data != step['steps']:
					act.data = step['steps']
					act.save()
			except:
				act = Activity()
				act.time = step['date']
				act.hour = int(step['hour'])
				act.type = 'steps'
				act.data = step['steps']
				act.patient = user
				act.save()
		response = {"success":1}
		json_response = json.dumps(response)
		return Ht(json_response, content_type = "application/json")
	else:
		return Ht(json.dumps({'success':2}), content_type = "application/json")
				
				
def getDaySteps(day_string, patient):
	returned_list = []
	step_list = Activity.objects.filter(type = "steps", patient = patient, time = day_string).order_by('hour')
	for step in step_list:
		returned_list.append(int(step.data))
	while len(returned_list) < 24:
		returned_list.append(0)
	return returned_list

def getDayPain(day_string, patient):
	returned_list = [[0 for x in range(24)],[[0] for x in range(24)]]
	pain_list = Pain.objects.filter(patient = patient, time = day_string).order_by('hour')
	for p in pain_list:
		returned_list[0][p.hour] = 1
		returned_list[1][p.hour] = json.loads(p.data)
		print returned_list[1]
	return returned_list
		
	
				
@csrf_exempt
def getActivity(request):
	if True:
		print request
		user = User.objects.get(session_key = request.GET['session_key'])
		patient = User.objects.get(name = request.GET['patient_username'])
		pair = Pair.objects.get(patient = patient)
		if pair.assigned_pt != user:
			response = {'success':0}
			json_response = json.dumps(response)
			return Ht(json_response, content_type = "application/json")
		else:
			response = {"success":1, "graphs":[]}
			now = datetime.datetime.strptime(request.GET['date'], "%Y-%m-%d").date()
			day = 0
			while day < 8:
				tmp = {}
				now_string = now.strftime("%Y-%m-%d")
				tmp['name'] = now.strftime("%A")
				[tmp_pain,tmp_data] = getDayPain(now_string,patient)
				tmp_activity = getDaySteps(now_string,patient)
				tmp['data'] = {'activity':tmp_activity, 'pain': tmp_pain, 'data':tmp_data}
				response['graphs'].append(tmp)
				now = now + datetime.timedelta(-1)
				print now
				day += 1
			response['graphs'] = response['graphs'][::-1]
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
		
'''
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

'''	

	