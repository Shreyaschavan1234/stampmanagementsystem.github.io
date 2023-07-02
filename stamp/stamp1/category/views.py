from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from category.models import Category

# Create your views here.
def index(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'Categories'
        stamp_cats = Category.objects.all()
        content['stamp_cats'] = stamp_cats
        if request.method == 'POST':
            name = request.POST['name']

            cat = Category()
            cat.name = name.title()
            cat.save()

            messages.success(request, f'{name.title()} added to categories.')
        return render(request, 'category/index.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def edit(request, pk):
    if request.session.has_key('account_id'):
        content = {}
        cat = Category.objects.get(pk=pk)
        content['title'] = f'Edit {cat.name}'
        content['cat'] = cat
        if request.method == 'POST':
            name = request.POST['name']
            cat.name = name.title()
            cat.save()

            messages.success(request, f'{name.title()} updated to categories.')
            return HttpResponseRedirect(reverse('stamp-cats'))
        return render(request, 'category/edit.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))