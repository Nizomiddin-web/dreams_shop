from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.views.generic import TemplateView
from unfold.contrib.filters.admin import RangeDateFilter, ChoicesDropdownFilter
from unfold.decorators import display
from unfold.views import UnfoldModelAdminViewMixin

from order.models import OrderItem, Order, StatusChoice
from unfold.admin import ModelAdmin, StackedInline

from payment.admin import PaymentTabular


# Register your models here.
class CustomBooleanFilter(SimpleListFilter):
    title = "To'lov qildimi?"
    parameter_name = 'is_paid'

    def lookups(self, request, model_admin):
        return [
            ('yes',"Ha"),
            ('no',"Yo'q")
        ]
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.filter(is_paid=True)
        elif self.value()=='no':
            return queryset.filter(is_paid=False)
        return queryset
#
# class OrderCustomPageView(UnfoldModelAdminViewMixin,TemplateView):
#     title = 'Buyurtmalar statistic'
#     permission_required = ()
#     template_name = "admin/payment_stat.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # Filter form
#         filter_form = PaymentCustomForm(self.request.GET or None)
#         payment = Payment.objects.all()
#
#         if filter_form.is_valid():
#             start_date = filter_form.cleaned_data.get('start_date')
#             end_date = filter_form.cleaned_data.get('end_date')
#
#             if start_date:
#                 payment = payment.filter(payment_date__gte=start_date)
#             if end_date:
#                 payment = payment.filter(payment_date__lte=end_date)
#         total_payment = payment.aggregate(total_sum=Sum('amount'))['total_sum'] or 0
#         total_mail_payment = payment.filter(order__payment_method=PaymentMethodChoice.MAIL).aggregate(total_sum=Sum('amount'))['total_sum'] or 0
#         total_cash_payment = payment.filter(order__payment_method=PaymentMethodChoice.CASH).aggregate(total_sum=Sum('amount'))['total_sum'] or 0
#         total_card_payment = payment.filter(order__payment_method=PaymentMethodChoice.CARD).aggregate(total_sum=Sum('amount'))['total_sum'] or 0
#         context['filter_form'] = filter_form
#         context['total_payment'] = f"{int(total_payment):,}".replace(",", " ")
#         context['total_mail_payment'] = f"{int(total_mail_payment):,}".replace(",", " ")
#         context['total_cash_payment'] = f"{int(total_cash_payment):,}".replace(",", " ")
#         context['total_card_payment'] = f"{int(total_card_payment):,}".replace(",", " ")
#         return context


class OrderItemTabular(StackedInline):
    model = OrderItem
    autocomplete_fields = ['product']
    tab = True
    extra = 1


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['id','order','product','product_price','quantity','total_price','payment_type','get_is_paid','get_created_at']
    search_fields = ['id','order__id','order__customer__phone_number','product__name','product__category__name','product__color__name','product__size__name']
    autocomplete_fields = ['product']
    date_hierarchy = "created_at"
    raw_id_fields = ['order','product']
    list_disable_select_all = True
    list_filter_submit = True
    list_filter = ['product','order__is_paid']
    def get_created_at(self,obj):
        return obj.created_at

    get_created_at.short_description='Yaratilgan vaqti'

    def get_customer_phone(self,obj):
        return obj.order.customer.phone_number
    get_customer_phone.short_description = 'Telefon raqam'
    @display(description="Umumiy narxi")
    def total_price(self,obj):
        return f"{int(obj.total_price()):,}".replace(",", " ") + " so'm"
    @display(description="Mahsulot narxi")
    def product_price(self,obj):
        return f"{int(obj.product.price):,}".replace(","," ") + " so'm"
    @display(description="Sotilganmi?")
    def get_is_paid(self,obj):
        return "ha" if obj.order.is_paid else "yo'q"
    @display(description="To'lov turi")
    def payment_type(self,obj):
        return obj.order.payment_method if obj.order.payment_method else "yo'q"


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['id','get_customer_fullname','get_customer_phone','get_address','get_created_at','status_custom_color','payment_method','is_paid']
    search_fields = ['id','customer__phone_number','customer__first_name']
    inlines = [OrderItemTabular,PaymentTabular]
    list_display_links = ['get_customer_fullname']
    # list_editable = ['status']
    autocomplete_fields = ['customer','address']
    list_filter = [('status',ChoicesDropdownFilter),('created_at',RangeDateFilter),'payment_method',CustomBooleanFilter]
    list_filter_submit = True
    readonly_fields = ['total_price']

    def get_customer_phone(self,obj):
        return obj.customer.phone_number
    get_customer_phone.short_description = 'Telefon raqam'

    def get_created_at(self,obj):
        return obj.created_at

    get_created_at.short_description='Yaratilgan vaqti'

    @display(
        description="Status",
        ordering="status",
        label={
            StatusChoice.PENDING: "info",
            StatusChoice.DELIVERED: 'success',
            StatusChoice.CANCELED: 'danger',
            StatusChoice.SHIPPED: 'warning',
            StatusChoice.GET_TOMORROW: 'warning',
            StatusChoice.HOLD: 'neutral',
        }
    )
    def status_custom_color(self,obj):
        return obj.status, obj.get_status_display()

    def get_customer_fullname(self,obj):
        return obj.customer.full_name()
    get_customer_fullname.short_description = 'Mijoz'

    def get_address(self,obj):
        return f"{obj.address.city}, {obj.address.state}, {obj.address.address_line}"

    get_address.short_description = 'Address'

    def get_readonly_fields(self, request, obj=None):
        # Agar yozuv mavjud bo'lsa va shartlar bajarilsa
        if obj and obj.is_paid and obj.status == StatusChoice.DELIVERED:
            # Barcha maydonlarni faqat o'qiladigan qilish
            return [field.name for field in self.model._meta.fields]
        elif obj and obj.status==StatusChoice.CANCELED:
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)
