from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import *
from django.template import loader
from oauth2client.client import OAuth2WebServerFlow
from .models import User

from datetime import datetime, timedelta

def index(request):
  #template = loader.get_template('polls/index.html')
  #return HttpResponse('sdfsdfsdfsdf')
  return render(request, 'dbank_api/index.html')

def auth(request):
  flow = OAuth2WebServerFlow(client_id='8de01e53-cdbf-48ee-a3e5-cf95046065c1',

                             client_secret='APbhxDPiJOyTLVS096VTQCKBsItdXVzrBYXsqhLhkC3s4gdRIiuZVx0LC-o8Ler0kYizJFsfE7wjCPlVGbx3cUA',

                             scope='read_accounts',

                             redirect_uri='http://localhost:8000/dbank_api/auth_return',

                             response_type='token',

                             auth_uri = 'https://simulator-api.db.com/gw/oidc/authorize')

  auth_uri = flow.step1_get_authorize_url()
  return HttpResponseRedirect(auth_uri)

def auth_return(request):
  if 'access_token' in request.GET:
    u = User(access_token=request.GET['access_token'],
             token_expiration=datetime.now() + timedelta(seconds=int(request.GET['expires_in'])))
    u.save()
  return render(request, 'dbank_api/auth_return.html')