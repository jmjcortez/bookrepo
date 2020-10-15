from django.db import models
from django.contrib import auth
from django_countries.fields import CountryField


class User(auth.models.User):
  country = CountryField() # equivalent to models.CharField(max_length=100, choices=TUPLE_OF_COUNTRY_CHOICES)