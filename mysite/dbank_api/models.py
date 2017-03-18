from django.db import models

class User(models.Model):
  first_name = models.CharField(max_length=30, null=True)
  last_name = models.CharField(max_length=50, null=True)
  email = models.CharField(max_length=50, null=True)
  access_token = models.CharField(max_length=400, null=True)
  token_expiration = models.DateTimeField(null=True)