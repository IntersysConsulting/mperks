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
	hh_id = models.FloatField(null=True)
        four_digit_pin = models.IntegerField()	

class Offer(models.Model):
	purchase_category = models.CharField(max_length = 25)
	reward_category = models.CharField(max_length = 25)
	reward_amount = models.FloatField()
	purchase_amount = models.FloatField()
	expiration = models.DateField()
	activated = models.BooleanField()
	progress = models.IntegerField()
	hh_id = models.FloatField()
	offer_id = models.FloatField()
	offer_rank_order_id = models.FloatField()
	offer_achieved_indicator = models.IntegerField()
	offer_generated_date = models.DateField()
	shopper = models.ForeignKey('Shopper')
	supercategory = models.CharField(max_length = 30)
	personalized = models.CharField(max_length=1)
	offer_rank_order_id = models.FloatField()


	

	

