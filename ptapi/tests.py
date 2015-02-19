from django.test import TestCase
import views

class Request():
    def __init__(self):
		self.POST = {'data': [{'date':'1', 'hour':'2', 'steps':'90'}]}

r = Request()
#print views.getPatientsExerciseData(r)
print views.addSteps(r)


patient = views.User.objects.get(name = 'joe')
act_log = views.Activity.objects.filter(patient = patient)
for a in act_log:
	print a.data + '-' + a.time		
def printPains():
	patient = views.User.objects.get(name = "joe")
	pain_log = views.Pain.objects.filter(patient = patient)
	print pain_log
	
#printPains()

# Create your tests here.
