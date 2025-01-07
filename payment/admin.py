from typing import List

from django.contrib import admin
from django.db.models import Sum
from django.urls import URLPattern, path
from django.views.generic import TemplateView
from unfold.admin import ModelAdmin, StackedInline
from unfold.views import UnfoldModelAdminViewMixin

from order.forms import OrderFilterForm
from order.models import Order, PaymentMethodChoice
from payment.forms import PaymentCustomForm
from payment.models import Payment
from product.models import Product


class PaymentCustomPageView(UnfoldModelAdminViewMixin,TemplateView):
    title = 'Payment statistic'
    permission_required = ()
    template_name = "admin/payment_stat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter form
        filter_form = PaymentCustomForm(self.request.GET or None)
        payment = Payment.objects.all()
        # product = Product.objects.all()
        if filter_form.is_valid():
            start_date = filter_form.cleaned_data.get('start_date')
            end_date = filter_form.cleaned_data.get('end_date')
            product_fl = filter_form.cleaned_data.get('product')
            # if product_fl:
            #     order_items = product.filter(id=product_fl).firts().items.all()
            if start_date:
                payment = payment.filter(payment_date__gte=start_date)
            if end_date:
                payment = payment.filter(payment_date__lte=end_date)
        total_payment = payment.aggregate(total_sum=Sum('amount'))['total_sum'] or 0
        total_mail_payment = payment.filter(order__payment_method=PaymentMethodChoice.MAIL).aggregate(total_sum=Sum('amount'))['total_sum'] or 0
        total_cash_payment = payment.filter(order__payment_method=PaymentMethodChoice.CASH).aggregate(total_sum=Sum('amount'))['total_sum'] or 0
        total_card_payment = payment.filter(order__payment_method=PaymentMethodChoice.CARD).aggregate(total_sum=Sum('amount'))['total_sum'] or 0
        context['filter_form'] = filter_form
        context['total_payment'] = f"{int(total_payment):,}".replace(",", " ")
        context['total_mail_payment'] = f"{int(total_mail_payment):,}".replace(",", " ")
        context['total_cash_payment'] = f"{int(total_cash_payment):,}".replace(",", " ")
        context['total_card_payment'] = f"{int(total_card_payment):,}".replace(",", " ")
        return context

class PaymentTabular(StackedInline):
    model = Payment
    readonly_fields = ['amount']
    tab = True
    extra = 0

@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ['id','order','get_amout']
    list_display_links = ['id','order']
    def get_amout(self, obj):
        return f"{int(obj.amount):,}".replace(",", " ") + " so'm"

    get_amout.short_description = "To'lov summasi"

    def get_urls(self) -> List[URLPattern]:
        return super().get_urls()+[
            path(
                "statistika",
                PaymentCustomPageView.as_view(model_admin=self),
                name="payment_payment_stat"
            )
        ]