from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from stamp.models import Stamp, StampType
from purchase.models import Purchase
from location.models import Location
from datetime import date, time, datetime
from django.db.models import Q

# Create your views here.
def index(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'Purchases'
        purchases = Purchase.objects.all().order_by('-id')
        content['purchases'] = purchases
        return render(request, 'purchase/index.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def create(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'New purchase'
        locations = Location.objects.all()
        stamp_types = StampType.objects.all()
        content['locations'] = locations
        content['stamp_types'] = stamp_types

        if request.method == 'POST':
            purchase = Purchase()
            purchase.location = Location.objects.get(pk = int(request.POST['location']))
            purchase.stamp_type = StampType.objects.get(pk = int(request.POST['stamp_type']))
            purchase.code = request.POST['code'].upper()
            purchase.series_start = int(request.POST['series_start'])
            purchase.series_end = int(request.POST['series_end'])
            purchase.quantity = int(request.POST['total_qty'])
            purchase.amount = int(request.POST['purchase_price'])
            purchase.total = int(request.POST['total_amount'])
            purchase.date = date.today().strftime("%Y-%m-%d")
            purchase.save()

            series_start = int(request.POST['series_start'])
            series_end = int(request.POST['series_end'])
            for i in range(series_start, series_end + 1):
                stamp = Stamp()
                stamp.stamp_type = StampType.objects.get(pk = int(request.POST['stamp_type']))
                stamp.location = Location.objects.get(pk = int(request.POST['location']))
                stamp.code = request.POST['code'].upper()
                stamp.number = i
                stamp.code_number = request.POST['code'].upper() + str(i)
                stamp.base_amount = int(request.POST['purchase_price'])
                stamp.save()

            messages.success(request, "Stamp purchase data created")
            return HttpResponseRedirect(reverse('purchase-index'))
        
        # # Last pending purchase
        # pending_purchase = Purchase.objects.filter(status = False).last()
        # if pending_purchase:
        #     last_id = Purchase.objects.latest('id')
        #     return HttpResponseRedirect(reverse('purchase-next', args=(int(last_id.id),)))

        # if request.method == 'POST':
        #     purchase = Purchase()
        #     purchase.location = Location.objects.get(pk = int(request.POST['location']))
        #     purchase.date = date.today()
        #     purchase.time = datetime.now().time()
        #     purchase.save()

        #     last_id = Purchase.objects.latest('id')
        #     return HttpResponseRedirect(reverse('purchase-next', args=(int(last_id.id),)))
        return render(request, 'purchase/create.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

# def next_page(request, pk):
#     if request.session.has_key('account_id'):
#         content = {}
#         content['title'] = 'Purchase #' + str(pk)
        
#         purchase = Purchase.objects.get(pk=pk)
#         if purchase.status == True:
#             messages.error(request, 'Please select the location first')
#             return HttpResponseRedirect(reverse('purchase-create'))
#         else:
#             content['purchase'] = purchase
#             stamp_types = StampType.objects.all()
#             content['stamp_types'] = stamp_types

#             purchase_list = StampPurchase.objects.filter(purchase_id = pk)
#             content['purchase_list'] = purchase_list

#             if request.method == 'POST':
#                 stamp_type = int(request.POST['stamp_type'])
#                 code = request.POST['code'].upper()
#                 series_start = int(request.POST['series_start'])
#                 series_end = int(request.POST['series_end'])
#                 qty = int(request.POST['total_qty'])
#                 price = float(request.POST['purchase_price'])
#                 amount = float(request.POST['total_amount'])

#                 check_pre_records = Stamp.objects.filter(Q(number__gte=series_start, number_lte=series_end), code = code, stamp_type_id = stamp_type).count()
#                 print(check_pre_records)
#                 if check_pre_records > 0:
#                     messages.error(request, 'Series record already exists')
#                 else:
#                     stamp_purchase = StampPurchase()
#                     stamp_purchase.purchase = Purchase.objects.get(pk=pk)
#                     stamp_purchase.stamp_type = StampType.objects.get(pk=stamp_type)
#                     stamp_purchase.purchase_price = price
#                     stamp_purchase.amount = amount
#                     stamp_purchase.initial_code = code
#                     stamp_purchase.location = Location.objects.get(pk=int(purchase.location_id))
#                     stamp_purchase.series_start = series_start
#                     stamp_purchase.series_end = series_end
#                     stamp_purchase.quantity = qty
#                     stamp_purchase.date = date.today()
#                     stamp_purchase.time = datetime.now().time()
#                     stamp_purchase.save()

#         return render(request, 'purchase/next.html', content)
#     else:
#         messages.error(request, "Please login first.")
#         return HttpResponseRedirect(reverse('login'))