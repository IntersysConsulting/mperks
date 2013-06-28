from django.shortcuts import render_to_response
from forms import NewShopperForm
from meijer.models import Shopper,Offer
from django.template import Context,Template, RequestContext
from django.core.context_processors import csrf
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError


def signin(request):
    data_dictionary={}
    mobile_number = request.POST['mobile_number']
    four_digit_pin = request.POST['four_digit_pin']
    user = authenticate(username=mobile_number, password=four_digit_pin)
    if user is not None:
        if user.is_active:
            login(request, user)
    else:
	data_dictionary['message']= "Mobile number not found or password incorrect, try to sign in again"
	return render_to_response("index.html", data_dictionary,context_instance=RequestContext(request))
    shopper = Shopper.objects.get(user=user)
    data_dictionary['first_name']= shopper.first_name
    return render_to_response("rewards.html", data_dictionary,context_instance=RequestContext(request))

def newuser(request):
    form = NewShopperForm()
    data_dictionary = {'form':form}
    return render_to_response("newuser.html", data_dictionary,context_instance=RequestContext(request))

def create_or_update(request):
    data_dictionary= {}
    if request.method == 'POST':
	form = NewShopperForm(request.POST)
	if form.is_valid():
	    try:
	        user = User.objects.get(username = request.POST['mobile_number'])
	    except User.DoesNotExist:
	        user = None
	    if user is not None:
	        form = NewShopperForm()
	        data_dictionary = {'form':form}
	        data_dictionary['message'] = "An account is already registered to that mobile number, please try another"
	        return render_to_response("newuser.html", data_dictionary,context_instance=RequestContext(request))
            else:
                user = User.objects.create_user(request.POST['mobile_number'], request.POST['email'],request.POST['four_digit_pin'])
	        user.save()
                shopper = Shopper.objects.create(user= user, first_name = form.cleaned_data['first_name'], last_name= form.cleaned_data['last_name'], mobile_number = form.cleaned_data['mobile_number'], zip_code= int(form.cleaned_data['zip_code']), email = form.cleaned_data['email'], four_digit_pin = int(form.cleaned_data['four_digit_pin']))
                shopper.save()
		data_dictionary['message'] = "Your account has been created, sign in to start saving!"
	else:
	    form = NewShopperForm()
            data_dictionary = {'form':form}
            data_dictionary['message'] = "One or more fields were empty, please fill out all fields"
            return render_to_response("newuser.html", data_dictionary,context_instance=RequestContext(request))
    return render_to_response("index.html", data_dictionary,context_instance=RequestContext(request))

def activate(request):
    data_dictionary = {}
    if request.method == 'POST':
	if 'offer1' in request.POST:
            offer1 = Offer.objects.get(purchase_category="Frozen Foods")
	    offer1.activated = True
	    offer1.save()
	elif 'offer2' in request.POST:
            offer2 = Offer.objects.get(purchase_category="Garden & Floral")
            offer2.activated = True
            offer2.save()
	elif 'offer3' in request.POST:
            offer3 = Offer.objects.get(purchase_category = "Apparel")
	    offer3.activated = True
	    offer3.save()
    offer1 = Offer.objects.get(purchase_category="Frozen Foods")
    offer2 = Offer.objects.get(purchase_category="Garden & Floral")
    offer3 = Offer.objects.get(purchase_category = "Apparel")
    data_dictionary = {'offer1': {"reward_amount":offer1.reward_amount, "reward_category" : offer1.reward_category, "purchase_amount": offer1.purchase_amount, "purchase_category": offer1.purchase_category, "activated": offer1.activated, "expiration": offer1.expiration, "progress": offer1.progress}, 'offer2': {"reward_amount":offer2.reward_amount, "reward_category" : offer2.reward_category, "purchase_amount": offer2.purchase_amount, "purchase_category": offer2.purchase_category, "activated": offer2.activated, "expiration": offer2.expiration, "progress": offer2.progress}, 'offer3': {"reward_amount":offer3.reward_amount, "reward_category" : offer3.reward_category, "purchase_amount": offer3.purchase_amount, "purchase_category": offer3.purchase_category, "activated": offer3.activated, "expiration": offer3.expiration, "progress": offer3.progress}}

    return render_to_response("rewards.html", data_dictionary,context_instance=RequestContext(request)) 

def rewards(request):
    offer1 = Offer.objects.get(purchase_category="Frozen Foods")
    offer2 = Offer.objects.get(purchase_category="Garden & Floral")
    offer3 = Offer.objects.get(purchase_category = "Apparel")
    offer1.activated = False
    offer1.save()
    offer2.activated = False
    offer2.save()
    offer3.activated = False
    offer3.save()
    data_dictionary = {'offer1': {"reward_amount":offer1.reward_amount, "reward_category" : offer1.reward_category, "purchase_amount": offer1.purchase_amount, "purchase_category": offer1.purchase_category, "activated": offer1.activated, "expiration": offer1.expiration, "progress": offer1.progress}, 'offer2': {"reward_amount":offer2.reward_amount, "reward_category" : offer2.reward_category, "purchase_amount": offer2.purchase_amount, "purchase_category": offer2.purchase_category, "activated": offer2.activated, "expiration": offer2.expiration, "progress": offer2.progress}, 'offer3': {"reward_amount":offer3.reward_amount, "reward_category" : offer3.reward_category, "purchase_amount": offer3.purchase_amount, "purchase_category": offer3.purchase_category, "activated": offer3.activated, "expiration": offer3.expiration, "progress": offer3.progress}}

    return render_to_response("rewards.html", data_dictionary,context_instance=RequestContext(request))

def signout(request):
    logout(request)
    data_dictionary ={}
    return render_to_response("index.html", data_dictionary,context_instance=RequestContext(request))

def index(request):
    data_dictionary ={}
    return render_to_response("index.html", data_dictionary,context_instance=RequestContext(request))

