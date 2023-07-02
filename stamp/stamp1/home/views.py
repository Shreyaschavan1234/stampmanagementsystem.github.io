from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from stamp.models import Stamp
from purchase.models import Purchase
from datetime import date, datetime
import time

# Create your views here.
def index(request):
    if request.session.has_key('account_id'):        
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += str(ele) + ", "
    # return string
    return str1

def dashboard(request):
    if request.session.has_key('account_id'):
        content = {}
        # months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        months_int = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        overall_sales = Stamp.objects.filter(sold=True)

        currentYear = datetime.now().year
        currentYear_sale = 0
        for sale in overall_sales:
            if sale.date.year == currentYear:
                currentYear_sale += sale.total_amount

        online_amount = 0
        cash_amount = 0
        for sale in overall_sales:
            if sale.paid_with != 'Cash':
                online_amount += sale.total_amount
            else:
                cash_amount += sale.total_amount

        sales_data = []
        for m in months_int:
            sale_amount = 0
            for sale in overall_sales:
                if sale.date.strftime('%m') == m:
                    sale_amount += sale.additional_amount
            sales_data.append(sale_amount)

        # content['months'] = listToString(months)
        content['sales'] = listToString(sales_data)
        content['current_year_sales'] = currentYear_sale
        content['online_amount'] = online_amount
        content['cash_amount'] = cash_amount

        overall_purchase = Purchase.objects.all()
        purchase_data = []
        for m in months_int:
            purchase_amount = 0
            for sale in overall_purchase:
                if sale.date.strftime('%m') == m:
                    purchase_amount += sale.total
            purchase_data.append(purchase_amount)

        # content['months'] = listToString(months)
        content['purchases'] = listToString(purchase_data)
                    

        content['title'] = 'Hi, Admin!'
        today_date = date.today().strftime("%Y-%m-%d")
        content['today_date'] = today_date
        content['available_stamps'] =  Stamp.objects.filter(sold=False).count()

        today_purchases = Purchase.objects.filter(date=today_date)
        today_sold =  Stamp.objects.filter(sold=True, date=today_date)
        # Get amount
        content['today_purchases_amount'] = sum(today_purchases.values_list('total', flat=True))
        content['today_sold_amount'] = sum(today_sold.values_list('additional_amount', flat=True))
        content['today_sells_amount'] = sum(today_purchases.values_list('total', flat=True)) - sum(today_sold.values_list('total_amount', flat=True))

        content['today_purchases'] = sum(today_purchases.values_list('quantity', flat=True))
        content['today_sold'] = today_sold.count()
        return render(request, 'dashboard.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))

def about(request):
    if request.session.has_key('account_id'):
        content = {}
        content['title'] = 'About project'
        return render(request, 'about.html', content)
    else:
        messages.error(request, "Please login first.")
        return HttpResponseRedirect(reverse('login'))