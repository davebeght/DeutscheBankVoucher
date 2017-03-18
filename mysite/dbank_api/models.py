from django.db import models

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


class Transactions(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  origin_iban = models.CharField(max_length=30, null=True)
  amount = models.FloatField(null=True)
  counter_party_name = models.CharField(max_length=100, null=True)
  usage = models.CharField(max_length=300, null=True)
  booking_date = models.DateField(null=True)
