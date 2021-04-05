from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
def home(request):
    #template = loader.get_template('index1.html')
   # return HttpResponse(template.render())
    return render(request,"index1.html")
def about(request):
    return render(request,"about_us.html")

def artists(request):
    return render(request,"artists.html")

def map(request):
    return render(request,"map.html")

def login(request):
    return render(request,"login.html")

def signup(request):
    return render(request,"signup.html")

def select(request):
    return render(request,"select.html")

def events(request):
	return render(request,"events.html")

def contact(request):
	return render(request,"contact.html")

def event(request):
	return render(request,"events.html")

def details(request):
    return render(request,"details.html")

def select(request):
    return render(request,"select.html")

def event_add(request):
    return render(request,"add_event.html")