import json
import random

from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Sum
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from customer.models import Customer
from order.models import Order, StatusChoice, PaymentMethodChoice
from payment.models import Payment
from product.models import Product


# Create your views here.

def dashboard_callback(request, context):
    ##########################
    #Payment Statistika
    ##########################
    total_sum = Payment.objects.aggregate(total_sum=Sum('amount'))['total_sum']
    cash_total_sum = Payment.objects.filter(order__payment_method=PaymentMethodChoice.CASH).aggregate(total_sum=Sum('amount'))['total_sum']
    card_total_sum = Payment.objects.filter(order__payment_method=PaymentMethodChoice.CARD).aggregate(total_sum=Sum('amount'))['total_sum']
    mail_total_sum = Payment.objects.filter(order__payment_method=PaymentMethodChoice.MAIL).aggregate(total_sum=Sum('amount'))['total_sum']
    total_sum = f"{int(total_sum if total_sum else 0):,}".replace(",", " ") + " so'm"
    cash_total_sum = f"{int(cash_total_sum if cash_total_sum else 0):,}".replace(",", " ") + " so'm"
    card_total_sum = f"{int(card_total_sum if card_total_sum else 0):,}".replace(",", " ") + " so'm"
    mail_total_sum = f"{int(mail_total_sum if mail_total_sum else 0):,}".replace(",", " ") + " so'm"
    ###########################
    #Umumiy statistika
    ###########################
    product_count = Product.objects.all().count()
    order_count = Order.objects.all().count()
    customer_count = Customer.objects.all().count()
    pending_order_count = Order.objects.filter(status=StatusChoice.PENDING).count()
    all_order_count = Order.objects.all().count()
    ###########################
    #Order Statistic
    ###########################

    context.update(
        {
            "product_count":product_count,
            "order_count":order_count,
            "customer_count":customer_count,
            "total_order_value":0,
            "payed_sum":total_sum,
            "pending_order_count":pending_order_count,
            "all_order_count":all_order_count,
            "cash_total_sum":cash_total_sum,
            "card_total_sum":card_total_sum,
            "mail_total_sum":mail_total_sum
        }
    )
    return context