from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from customer.models import Customer
import base64
from django.core.files.base import ContentFile
import time

# Create your views here.
def index(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'Customers'
        customers = Customer.objects.all()
        content['customers'] = customers
        return render(request, 'customer/index.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def create(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'Create new customers'
        if request.method == 'POST':
            name = request.POST['name']
            aadhaar = int(request.POST['aadhaar'])
            mobile = int(request.POST['mobile'])
            location = request.POST['location']
            state = request.POST['state']
            tehsil = request.POST['tehsil']
            district = request.POST['district']
            pincode = int(request.POST['pincode'])

            check_aadhaar = Customer.objects.filter(aadhaar = aadhaar).first()
            if check_aadhaar:
                messages.error(request, f"Customer with {aadhaar} aadhaar aleady exists.")
            else:
                customer = Customer()
                customer.name = name.title()
                customer.aadhaar = aadhaar
                customer.mobile = mobile
                customer.town = location.title()
                customer.state = state.title()
                customer.tehsil = tehsil.title()
                customer.district = district.title()
                customer.pincode = pincode
                customer.save()

                last_customer = Customer.objects.filter(aadhaar=aadhaar, mobile=mobile).first()

                messages.success(request, f"{name.title()} added to customers. Add an image for the customer now.")
                # return HttpResponseRedirect(reverse('customer-index'))
                return HttpResponseRedirect(reverse('customer-camera', args=(int(customer.id),)))
        return render(request, 'customer/create.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def edit(request, pk):
    if request.session.has_key('account_id'):
        content = {}
        customer = Customer.objects.get(pk=pk)
        content['title'] = f'Edit {customer.name}'
        content['customer'] = customer
        if request.method == 'POST':
            name = request.POST['name']
            aadhaar = int(request.POST['aadhaar'])
            mobile = int(request.POST['mobile'])
            location = request.POST['location']
            state = request.POST['state']
            tehsil = request.POST['tehsil']
            district = request.POST['district']
            pincode = int(request.POST['pincode'])

            customer.name = name.title()
            customer.aadhaar = aadhaar
            customer.mobile = mobile
            customer.town = location.title()
            customer.state = state.title()
            customer.tehsil = tehsil.title()
            customer.district = district.title()
            customer.pincode = pincode
            customer.save()

            messages.success(request, f"{name.title()} updated to customers.")
            return HttpResponseRedirect(reverse('customer-index'))
                
        return render(request, 'customer/edit.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def camera(request, pk):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'Image of customer'
        customer = Customer.objects.get(pk=pk)
        content['customer'] = customer
        is_return = request.GET.get("return")
        content['is_return'] = is_return
        if request.method == 'POST':
            print(is_return)
            image = request.POST['image_data']
            format, imgstr = image.split(';base64,') 
            ext = format.split('/')[-1]
            filename = str(int(time.time())) + '.' + ext
            data = ContentFile(base64.b64decode(imgstr), name=filename)
            customer.image = data
            customer.save()
            if is_return:
                return HttpResponseRedirect(reverse('customer-index'))
            else:
                return HttpResponseRedirect(reverse('sell-customer', args=(int(customer.id),)))
        return render(request, 'customer/image.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))