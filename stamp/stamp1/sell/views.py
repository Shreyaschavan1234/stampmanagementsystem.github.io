from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from stamp.models import Stamp, StampType
from purchase.models import Purchase
from location.models import Location
from datetime import date, datetime
import time
from django.db.models import Q
from customer.models import Customer
import json
from django.core.serializers import serialize
from django.http import JsonResponse
from category.models import Category

# Create your views here.
def index(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'Sells'
        content['sells'] = Stamp.objects.filter(sold=True).order_by('-datetime')
        return render(request, 'sell/index.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))
    

def create(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'New Sell'
        content['customers'] = None
        content['customers_count'] = -1
        if request.method == 'POST':
            search = request.POST['search']
            get_customers = Customer.objects.filter(Q(mobile=search) | Q(aadhaar=search))
            print(get_customers)
            content['customers'] = get_customers
            content['customers_count'] = get_customers.count()
        return render(request, 'sell/create.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def customer(request, pk):
    if request.session.has_key('account_id'):
        content = {}
        customer = Customer.objects.get(pk=pk)
        content['title'] = 'Sell stamp to ' + customer.name
        content['customer'] = customer
        stamp_types = StampType.objects.all()
        content['stamp_types'] = stamp_types
        content['categories'] = Category.objects.all()
        content['locations'] = Location.objects.all()

        if request.method == 'POST':
            hd_stamp_id = int(request.POST['hd_stamp_id'])
            
            stamp = Stamp.objects.get(pk=hd_stamp_id)
            stamp.sold = True
            stamp.customer = Customer.objects.get(pk=pk)
            stamp.base_amount = stamp.stamp_type.base_price
            stamp.additional_amount = float(request.POST['additional_amount'])
            stamp.title = request.POST['title'].upper()
            stamp.purpose = request.POST['purpose'].upper()
            stamp.corresponding_person = request.POST['corresponding_person'].upper()
            # stamp.file = request.FILES['file']
            stamp.category = Category.objects.get(pk=int(request.POST['category']))
            stamp.total_amount = float(request.POST['additional_amount']) + stamp.stamp_type.base_price
            stamp.paid_with = request.POST['payment_mode']
            stamp.notes = request.POST['notes'].upper()
            stamp.date = date.today().strftime("%Y-%m-%d")
            stamp.time = time.strftime("%H:%M:%S")
            stamp.datetime = date.today().strftime("%Y-%m-%d") + ' ' + time.strftime("%H:%M:%S")
            stamp.save()

            messages.success(request, "Stamp sell record added.")
            return HttpResponseRedirect(reverse('sell-index'))

        return render(request, 'sell/customer.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def info(request, pk):
    if request.session.has_key('account_id'):
        content = {}
        sell = Stamp.objects.get(pk=pk)
        content['title'] = 'Sell info'
        content['sell'] = sell
        return render(request, 'sell/info.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))


# AJAX
def get_stamp_details(request):
    stamp_type_id = int(request.GET.get('stamp_type_id', None))
    stamp_details = Stamp.objects.filter(stamp_type_id = stamp_type_id, sold = False).first()
    # data = json.loads(serialize('python', [stamp_details]))
    data = serialize('python', [stamp_details])
    return JsonResponse(data, safe = False)