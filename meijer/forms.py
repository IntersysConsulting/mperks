from django.forms import ModelForm, ModelMultipleChoiceField, ChoiceField, CharField
from meijer.models import Shopper 

class NewShopperForm(ModelForm):

	class Meta:
		model = Shopper
		fields=('first_name','last_name', 'mobile_number', 'four_digit_pin', 'zip_code', 'email')

		
		
