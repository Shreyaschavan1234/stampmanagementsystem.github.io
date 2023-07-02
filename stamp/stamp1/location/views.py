from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from location.models import Location

# Create your views here.
def index(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'Locations'
        locations = Location.objects.all()
        content['locations'] = locations
        if request.method == 'POST':
            name = request.POST['name']
            
            location = Location()
            location.name = name.title()
            location.save()
            messages.success(request, f'{name.title()} saved in location.')
        return render(request, 'location/index.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def edit(request, pk):
    if request.session.has_key('account_id'):
        content = {}
        location = Location.objects.get(pk=pk)
        content['location'] = location
        content['title'] = f'Edit {location.name} location'
        if request.method == 'POST':
            name = request.POST['name']
            location.name = name.title()
            location.save()
            messages.success(request, f'{name.title()} updated in location.')
            return HttpResponseRedirect(reverse('location-index'))
        return render(request, 'location/edit.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))