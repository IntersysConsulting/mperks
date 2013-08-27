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
from itertools import chain
from decimal import Decimal, ROUND_DOWN


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
    shopper = Shopper.objects.get(user= request.user)
    if shopper.offer_set.count() == 0 and shopper.hh_id == 99999999999:
        hs_offers0 = Offer.objects.filter(supercategory = 'SOFTLINES', personalized = 'D')[:2]
	hs_offers1 = Offer.objects.filter(supercategory = 'IN AND OUTDOOR HOME', personalized = 'D')[:2]
        hs_offers2 = Offer.objects.filter(supercategory = 'MISC.', personalized = 'D')[:2]
        hs_offers3 = Offer.objects.filter(supercategory = 'SYSTEM', personalized = 'D')[:2]
        hs_offers4 = Offer.objects.filter(supercategory = 'HARDLINES', personalized = 'D')[:2]
        hs_offers5 = Offer.objects.filter(supercategory = 'SUPPLIES AND PACKAGING', personalized = 'D')[:2]
	hs_offers = list(chain(hs_offers0, hs_offers1, hs_offers2, hs_offers3, hs_offers4, hs_offers5))
        for offer in hs_offers:
	    offer.shopper = shopper
	    offer.supercategory = 'Hardlines and Softlines'
	    offer.pk = None
	    offer.save()

        dpc_offers0 = Offer.objects.filter(supercategory = 'DRUG STORE', personalized = 'D')[:5]
        dpc_offers1 = Offer.objects.filter(supercategory = 'PETS AND CONSUMABLES', personalized = 'D')[:5]
	dpc_offers = list(chain(dpc_offers0, dpc_offers1))
        for offer in dpc_offers:
	    offer.shopper = shopper
	    offer.supercategory = 'Drug, Pets and Consumables'
	    offer.pk = None
	    offer.save()

        gf_offers0 = Offer.objects.filter(supercategory = 'FRESH', personalized = 'D')[:5]
        gf_offers1 = Offer.objects.filter(supercategory = 'GROCERY', personalized = 'D')[:5]
	gf_offers = list(chain(gf_offers0, gf_offers1))
        for offer in gf_offers:
	    offer.shopper = shopper
	    offer.supercategory = 'Grocery and Fresh'
     	    offer.pk = None
	    offer.save()


    data_dictionary['first_name']= shopper.first_name
    return render_to_response("index.html", data_dictionary,context_instance=RequestContext(request))

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
                shopper = Shopper.objects.create(user= user, first_name = form.cleaned_data['first_name'], last_name= form.cleaned_data['last_name'], mobile_number = form.cleaned_data['mobile_number'], zip_code= int(form.cleaned_data['zip_code']), email = form.cleaned_data['email'], four_digit_pin = int(form.cleaned_data['four_digit_pin']),hh_id= 99999999999)
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
    shopper = Shopper.objects.get(user=request.user)
    if shopper.hh_id == 99999999999:
        offer1 = shopper.offer_set.filter(supercategory = 'Hardlines and Softlines').order_by('offer_rank_order_id')[:10]
        offer2 = shopper.offer_set.filter(supercategory = 'Drug, Pets and Consumables').order_by('offer_rank_order_id')[:10]
        offer3 = shopper.offer_set.filter(supercategory = 'Grocery and Fresh').order_by('offer_rank_order_id')[:10]
    else:
        hs_offers0 = Offer.objects.filter(supercategory = 'SOFTLINES', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers1 = Offer.objects.filter(supercategory = 'IN AND OUTDOOR HOME', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers2 = Offer.objects.filter(supercategory = 'MISC.', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers3 = Offer.objects.filter(supercategory = 'SYSTEM', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers4 = Offer.objects.filter(supercategory = 'HARDLINES', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers5 = Offer.objects.filter(supercategory = 'SUPPLIES AND PACKAGING', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        offer1 = list(chain(hs_offers0, hs_offers1, hs_offers2, hs_offers3, hs_offers4, hs_offers5))

        dpc_offers0 = Offer.objects.filter(supercategory = 'DRUG STORE', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:5]
        dpc_offers1 = Offer.objects.filter(supercategory = 'PETS AND CONSUMABLES', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:5]
        offer2 = list(chain(dpc_offers0, dpc_offers1))

        gf_offers0 = Offer.objects.filter(supercategory = 'FRESH', hh_id = shopper.hh_id).order_by('offer_rank_order_id')[:5]
        gf_offers1 = Offer.objects.filter(supercategory = 'GROCERY', hh_id = shopper.hh_id).order_by('offer_rank_order_id')[:5]
        offer3 = list(chain(gf_offers0, gf_offers1))
    offer1 = offer1[0]
    offer2 = offer2[0]
    offer3 = offer3[0]
    if request.method == 'POST':
	if 'offer1' in request.POST:
	    offer1.activated = True
	    offer1.shopper = shopper
	    offer1.progress = 20
	    offer1.save()
	elif 'offer2' in request.POST:
            offer2.activated = True
	    offer2.shopper = shopper
	    offer2.progress = 20
            offer2.save()
	elif 'offer3' in request.POST:
	    offer3.activated = True
	    offer3.shopper = shopper
	    offer3.progress = 20
	    offer3.save()
    reward_amount1 = Decimal(str(offer1.reward_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    reward_amount2 = Decimal(str(offer2.reward_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    reward_amount3 = Decimal(str(offer3.reward_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    purchase_amount1 = Decimal(str(offer1.purchase_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    purchase_amount2 = Decimal(str(offer2.purchase_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    purchase_amount3 = Decimal(str(offer3.purchase_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    data_dictionary = {'offer1': {"reward_amount":reward_amount1, "reward_category" : offer1.reward_category, "purchase_amount": purchase_amount1, "purchase_category": offer1.purchase_category, "activated": offer1.activated, "expiration": offer1.expiration, "progress": offer1.progress}, 'offer2': {"reward_amount":reward_amount2, "reward_category" : offer2.reward_category, "purchase_amount": purchase_amount2, "purchase_category": offer2.purchase_category, "activated": offer2.activated, "expiration": offer2.expiration, "progress": offer2.progress}, 'offer3': {"reward_amount":reward_amount3, "reward_category" : offer3.reward_category, "purchase_amount": purchase_amount3, "purchase_category": offer3.purchase_category, "activated": offer3.activated, "expiration": offer3.expiration, "progress": offer3.progress}}

    data_dictionary['first_name']= shopper.first_name
    return render_to_response("rewards.html", data_dictionary,context_instance=RequestContext(request)) 

def rewards(request):
    shopper = Shopper.objects.get(user=request.user)
    if shopper.hh_id == 99999999999:
    	offer1 = shopper.offer_set.filter(supercategory = 'Hardlines and Softlines').order_by('offer_rank_order_id')[:10]
    	offer2 = shopper.offer_set.filter(supercategory = 'Drug, Pets and Consumables').order_by('offer_rank_order_id')[:10]
    	offer3 = shopper.offer_set.filter(supercategory = 'Grocery and Fresh').order_by('offer_rank_order_id')[:10]
    else:
        hs_offers0 = Offer.objects.filter(supercategory = 'SOFTLINES', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers1 = Offer.objects.filter(supercategory = 'IN AND OUTDOOR HOME', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers2 = Offer.objects.filter(supercategory = 'MISC.', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers3 = Offer.objects.filter(supercategory = 'SYSTEM', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers4 = Offer.objects.filter(supercategory = 'HARDLINES', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        hs_offers5 = Offer.objects.filter(supercategory = 'SUPPLIES AND PACKAGING', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:2]
        offer1 = list(chain(hs_offers0, hs_offers1, hs_offers2, hs_offers3, hs_offers4, hs_offers5))

        dpc_offers0 = Offer.objects.filter(supercategory = 'DRUG STORE', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:5]
        dpc_offers1 = Offer.objects.filter(supercategory = 'PETS AND CONSUMABLES', hh_id = shopper.hh_id ).order_by('offer_rank_order_id')[:5]
        offer2 = list(chain(dpc_offers0, dpc_offers1))

        gf_offers0 = Offer.objects.filter(supercategory = 'FRESH', hh_id = shopper.hh_id).order_by('offer_rank_order_id')[:5]
        gf_offers1 = Offer.objects.filter(supercategory = 'GROCERY', hh_id = shopper.hh_id).order_by('offer_rank_order_id')[:5]
        offer3 = list(chain(gf_offers0, gf_offers1))


    offer1 = offer1[0]
    offer1.activated = False
    offer1.shopper = shopper
    offer1.save()
    offer2 = offer2[0]
    offer2.activated = False
    offer2.shopper = shopper
    offer2.save()
    offer3 = offer3[0]
    offer3.activated = False
    offer3.shopper = shopper
    offer3.save()
    reward_amount1 = Decimal(str(offer1.reward_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    reward_amount2 = Decimal(str(offer2.reward_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    reward_amount3 = Decimal(str(offer3.reward_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    purchase_amount1 = Decimal(str(offer1.purchase_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    purchase_amount2 = Decimal(str(offer2.purchase_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    purchase_amount3 = Decimal(str(offer3.purchase_amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    data_dictionary = {'offer1': {"reward_amount":reward_amount1, "reward_category" : offer1.reward_category, "purchase_amount": purchase_amount1, "purchase_category": offer1.purchase_category, "activated": offer1.activated, "expiration": offer1.expiration, "progress": offer1.progress}, 'offer2': {"reward_amount":reward_amount2, "reward_category" : offer2.reward_category, "purchase_amount": purchase_amount2, "purchase_category": offer2.purchase_category, "activated": offer2.activated, "expiration": offer2.expiration, "progress": offer2.progress}, 'offer3': {"reward_amount":reward_amount3, "reward_category" : offer3.reward_category, "purchase_amount": purchase_amount3, "purchase_category": offer3.purchase_category, "activated": offer3.activated, "expiration": offer3.expiration, "progress": offer3.progress}}

    data_dictionary['first_name']= shopper.first_name
    return render_to_response("rewards.html", data_dictionary,context_instance=RequestContext(request))

def signout(request):
    logout(request)
    data_dictionary ={}
    return render_to_response("index.html", data_dictionary,context_instance=RequestContext(request))

def index(request):
    data_dictionary = {}
#    if request.user is not None:
#    	shopper = Shopper.objects.get(user=request.user)
#    	data_dictionary['first_name']= shopper.first_name
    return render_to_response("index.html", data_dictionary,context_instance=RequestContext(request))

