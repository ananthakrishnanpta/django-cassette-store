from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader # this module helps load html template

# Create your views here.


# def home(request):
#     return HttpResponse("Hi, This is my home page !")

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def about(request):
    # return HttpResponse("Hi, this is my about page !!!")
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

