from django.test import TestCase
import views
import models


#views.createAchievements()
#views.deleteallachievements()
class Request():
    def __init__(self):
		self.POST = {'username':'joejoejoe', 'email':'joejoe', 'password':'joejoejoe', 'type':'patient'}



	
	
r = Request()
#print views.getPatientsExerciseData(r)
print views.register(r)

k = models.Activity.objects.filter()
ll = [(i.patient.name, i.hour) for i in k]
print ll

'''
patient = views.User.objects.get(name = 'joe')
act_log = views.Activity.objects.filter(patient = patient)
for a in act_log:
	print a.data + '-' + a.time		
def printPains():
	patient = views.User.objects.get(name = "joe")
	pain_log = views.Pain.objects.filter(patient = patient)
	print pain_log
'''	
#printPains()

# Create your tests here.
