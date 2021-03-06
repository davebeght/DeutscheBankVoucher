from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .data import Categories
from collections import Counter
import re
from .util import find_voucher

class User(models.Model):
  #basic user info
  first_name = models.CharField(max_length=30, null=True)
  last_name = models.CharField(max_length=50, null=True)
  male = models.NullBooleanField()
  date_of_birth = models.DateField(null=True)

  #dbank access information
  access_token = models.CharField(max_length=400, null=True)
  token_expiration = models.DateTimeField(null=True)

  #Adress
  street = models.CharField(max_length=50, null=True)
  house_number = models.CharField(max_length=8, null=True)
  zip = models.CharField(max_length=10, null=True)
  city = models.CharField(max_length=30, null=True)

  def get_keywords_and_categories(self):
    counted_set = build_dict(self.get_transactions())
    keywords = get_most_frequent_keywords(counted_set, 3)
    categories = get_categories(keywords)
    return keywords, categories

  def get_transactions(self):
    return Transaction.objects.filter(user=self).all()

  def get_vouchers(self):
    return Voucher.objects.filter(user=self).all() #TODO: apply filter

  def add_vouchers(self, keyword):
    data = find_voucher(self.city.lower(), keyword)
    for index, row in data.iterrows():
      v = Voucher(
        user=self,
        description = row['description'],
        image_url = 'http://' + row['imageUrl'],
        location = row['location'],
        merchant = row['merchant_name'],
        original_price = float(row['originalPrice'].replace(',','.')),
        new_price = float(row['new_price'].replace(',','.')),
        groupon_link = row['redirectUrl'],
        score = 1.0
      )
      v.save()


class Transaction(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  origin_iban = models.CharField(max_length=30, null=True)
  amount = models.FloatField(null=True)
  counter_party_name = models.CharField(max_length=100, null=True)
  usage = models.CharField(max_length=300, null=True)
  booking_date = models.DateField(null=True)

class Voucher(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  description = models.CharField(max_length=300, null=True)
  image_url = models.CharField(max_length=300, null=True)
  location = models.CharField(max_length=50, null=True)
  merchant = models.CharField(max_length=50, null=True)
  original_price = models.FloatField(null=True)
  new_price = models.FloatField(null=True)
  groupon_link = models.CharField(max_length=300, null=True)
  score = models.FloatField(null=True)


def get_most_frequent_keywords(countedSet, numberOfKeywords):
  keywordsList = []
  for entry in countedSet.most_common(numberOfKeywords):
    keywordsList.append(entry[0])
  return keywordsList

def get_categories(keywordsList):
  cat = Categories()
  foundCategories = set()

  for keyword in keywordsList:
    for key in cat.allCategories.keys():
      pattern = re.compile(".*"+keyword+".*", re.IGNORECASE)
      for value in cat.allCategories.get(key):
        if pattern.match(value) is not None:
          foundCategories.add(key)

  return list(foundCategories)

def build_dict(list):
 dict = []
 for t in list:
   dict.append(t.counter_party_name)
 return Counter(dict)
