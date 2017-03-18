from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  return HttpResponse("This should link to the Deutsche Bank authentication process")

