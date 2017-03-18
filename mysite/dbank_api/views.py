from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(request):
  #template = loader.get_template('polls/index.html')
  #return HttpResponse('sdfsdfsdfsdf')
  return render(request, 'dbank_api/index.html')

