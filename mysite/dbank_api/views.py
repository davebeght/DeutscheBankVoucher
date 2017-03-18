from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import *
from django.template import loader
from oauth2client.client import OAuth2WebServerFlow
from .models import User, Transaction
import requests
import json
from dateutil.parser import parse

from datetime import datetime, timedelta

def index(request):
  #template = loader.get_template('polls/index.html')
  #return HttpResponse('sdfsdfsdfsdf')
  return render(request, 'dbank_api/index.html')

def auth(request):
  flow = OAuth2WebServerFlow(client_id='8de01e53-cdbf-48ee-a3e5-cf95046065c1',

                             client_secret='APbhxDPiJOyTLVS096VTQCKBsItdXVzrBYXsqhLhkC3s4gdRIiuZVx0LC-o8Ler0kYizJFsfE7wjCPlVGbx3cUA',

                             scope='',

                             redirect_uri='http://localhost:8000/dbank_api/auth_return',

                             response_type='token',

                             auth_uri = 'https://simulator-api.db.com/gw/oidc/authorize')

  auth_uri = flow.step1_get_authorize_url()
  return HttpResponseRedirect(auth_uri)

def auth_return(request):
  if 'access_token' in request.GET:
    #save access token and token expiration datetime
    u = User(access_token=request.GET['access_token'],
             token_expiration=datetime.now() + timedelta(seconds=int(request.GET['expires_in'])))
    u.save()

    #make api calls for user
    transactions = access_endpoint(u, '/transactions')
    addresses = access_endpoint(u, '/addresses')
    cash_accounts = access_endpoint(u, '/cashAccounts')
    user_info = access_endpoint(u, '/userInfo')

    #save basic user information
    u.first_name = user_info['firstName']
    u.last_name = user_info['lastName']
    u.male = ('male' == user_info['gender'])
    u.date_of_birth = parse(user_info['dateOfBirth'])

    #save address
    if len(addresses) >= 1:
      i = 0
      u.city = addresses[i]['city']
      u.street = addresses[i]['street']
      u.house_number = addresses[i]['houseNumber']
      u.zip = addresses[i]['zip']

    u.save()

    #store transactions
    for transact in transactions:
      t = Transaction(
        user=u,
        origin_iban=transact['originIban'],
        amount=float(transact['amount']),
        counter_party_name=transact['counterPartyName'],
        usage=transact['usage'],
        booking_date=parse(transact['bookingDate'])
      )
      t.save()

  return render(request, 'dbank_api/auth_return.html')

def access_endpoint(user, endpoint):
  auth_header = {'Authorization': 'Bearer ' + str(user.access_token)}
  response = requests.get('https://simulator-api.db.com/gw/dbapi/v1' + endpoint, headers=auth_header)
  ledger_dict = json.loads(response.text)
  return ledger_dict