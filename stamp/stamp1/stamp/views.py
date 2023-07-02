from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from stamp.models import Stamp, StampType
from django_serverside_datatable.views import ServerSideDatatableView

# from django.http import HttpResponse
# from django.core import serializers

# def myModel_asJson(request):
#     object_list = Stamp.objects.all()
#     json = serializers.serialize('json', object_list)
#     return HttpResponse(json, content_type='application/json')

class ItemListView(ServerSideDatatableView):
	queryset = Stamp.objects.all()
	columns = ['id', 'location_id__name', 'stamp_type_id__name', 'code_number', 'base_amount', 'sold']

# Create your views here.
def stamp_types(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'Stamp types'
        stamp_types = StampType.objects.all()
        content['stamp_types'] = stamp_types
        if request.method == 'POST':
            name = request.POST['name']
            number = request.POST['number']
            price = request.POST['price']
            image = request.FILES['image']

            new_type = StampType()
            new_type.name = name.title()
            new_type.number = int(number)
            new_type.base_price = float(price)
            new_type.image = image
            new_type.save()

            messages.success(request, f'{name.title()} added to stamp types')
        return render(request, 'stamp/types/index.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def stamp_types_edit(request, pk):
    if request.session.has_key('account_id'):
        content = {}
        stamp_type = StampType.objects.get(pk=pk)
        content['title'] = f'Edit {stamp_type.name} stamp type'
        content['stamp_type'] = stamp_type
        if request.method == 'POST':
            name = request.POST['name']
            number = request.POST['number']
            price = request.POST['price']

            stamp_type.name = name.title()
            stamp_type.number = int(number)
            stamp_type.base_price = float(price)
            if 'image' in request.FILES:
                image = request.FILES['image']
                stamp_type.image = image
            stamp_type.save()

            messages.success(request, f'{name.title()} updated to stamp types')
            return HttpResponseRedirect(reverse('stamp-types'))
        return render(request, 'stamp/types/edit.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def index(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'Stamps'
        # stamps = None
        # if sold == 1:
        #     content['title'] = 'Sold Stamps'
        #     stamps = Stamp.objects.filter(sold=True).only('id','location', 'stamp_type', 'code_number', 'base_amount', 'sold')
        # else:
        #     content['title'] = 'Available Stamps'
        #     stamps = Stamp.objects.filter(sold=False).only('id','location', 'stamp_type', 'code_number', 'base_amount', 'sold')
        # content['stamps'] = stamps
        # content['sold'] = sold
        return render(request, 'stamp/index.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))