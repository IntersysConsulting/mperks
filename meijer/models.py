from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime


class Shopper(models.Model):
	user = models.OneToOneField(User, null=True, blank =True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	mobile_number = models.CharField(max_length=15)
	zip_code = models.IntegerField()
	email = models.EmailField()
        four_digit_pin = models.IntegerField()	

class Offer(models.Model):
	purchase_category = models.CharField(max_length = 25)
	reward_category = models.CharField(max_length = 25)
	reward_amount = models.IntegerField()
	purchase_amount = models.IntegerField()
	expiration = models.DateField()
	activated = models.BooleanField()
	progress = models.IntegerField()


	

	

