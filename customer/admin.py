import random
from datetime import timedelta

from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.db.models import Sum, Count
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.timezone import now
from import_export.admin import ImportExportModelAdmin

from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.components import BaseComponent, register_component
from unfold.contrib.filters.admin import FieldTextFilter, RangeDateTimeFilter
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import display

from customer.models import Customer, Address
from order.admin import OrderItemTabular
from order.models import Order, OrderItem
from product.models import Product

admin.site.unregister(User)
admin.site.unregister(Group)

class OrderTabular(StackedInline):
    model = Order
    tab = True

class AddressTabular(StackedInline):
    model = Address
    tab = True

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(ModelAdmin,ImportExportModelAdmin):
    export_form_class = ExportForm
    import_form_class = ImportForm
    # compressed_fields = True
    # list_fullwidth = True
    list_filter_submit = True
    warn_unsaved_form = True
    list_display = ['id','first_name','last_name','phone_number']
    list_display_links = ['id','first_name']
    list_filter = ['created_at',("first_name", FieldTextFilter)]
    list_horizontal_scrollbar_top = True
    search_fields = ['first_name','last_name','phone_number']
    list_per_page = 10

    # list_filter_sheet = False

@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ['id','city','address_line','phone']
    list_display_links = ['id','city','address_line']
    search_fields = ['city','address_line']
    list_per_page = 10
    # @display(description="Mijoz")
    # def customer_fullname(self,obj):
    #     return obj.customer.full_name()

    # @display(description="Telefon raqam")
    # def customer_phone(self,obj):
    #     return obj.customer.phone_number
    #

class CustomAdminSite(admin.AdminSite):
    site_header = "Statistika Paneli"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name="dashboard"),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Statistikani hisoblash
        product_count = Product.objects.count()
        order_count = Order.objects.count()
        customer_count = Customer.objects.count()
        total_order_value = OrderItem.objects.aggregate(Sum('price'))['price__sum'] or 0
        top_products = (
            Product.objects.annotate(total_orders=Count('orderitem'))
            .order_by('-total_orders')[:5]
        )

        context = {
            'product_count': product_count,
            'order_count': order_count,
            'customer_count': customer_count,
            'total_order_value': total_order_value,
            'top_products': top_products,
        }

        return TemplateResponse(request, "admin/dashboard.html", context)


# Custom admin saytni ishga tushirish
custom_admin_site = CustomAdminSite(name="custom_admin")


@register_component
class TrackerComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []

        for i in range(1, 72):
            has_value = random.choice([True, True, True, True, False])
            color = None
            tooltip = None
            if has_value:
                value = random.randint(2, 6)
                color = f"bg-primary-{value}00 dark:bg-primary-{9 - value}00"
                tooltip = f"Value {value}"

            data.append(
                {
                    "color": color,
                    "tooltip": tooltip,
                }
            )

        context["data"] = data
        return context


@register_component
class CohortComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = []
        headers = []
        cols = []

        dates = reversed(
            [(now() - timedelta(days=x)).strftime("%B %d, %Y") for x in range(8)]
        )
        groups = range(1, 10)

        for row_index, date in enumerate(dates):
            cols = []

            for col_index, _col in enumerate(groups):
                color_index = 8 - row_index - col_index
                col_classes = []

                if color_index > 0:
                    col_classes.append(
                        f"bg-primary-{color_index}00 dark:bg-primary-{9 - color_index}00"
                    )

                if color_index >= 4:
                    col_classes.append("text-white dark:text-gray-600")

                value = random.randint(
                    4000 - (col_index * row_index * 225),
                    5000 - (col_index * row_index * 225),
                )

                subtitle = f"{random.randint(10, 100)}%"

                if value <= 0:
                    value = 0
                    subtitle = None

                cols.append(
                    {
                        "value": value,
                        "color": " ".join(col_classes),
                        "subtitle": subtitle,
                    }
                )

            rows.append(
                {
                    "header": {
                        "title": date,
                        "subtitle": f"Total {sum(col['value'] for col in cols):,}",
                    },
                    "cols": cols,
                }
            )

        for index, group in enumerate(groups):
            total = sum(row["cols"][index]["value"] for row in rows)

            headers.append(
                {
                    "title": f"Group #{group}",
                    "subtitle": f"Total {total:,}",
                }
            )
        context["data"] = {
            "headers": headers,
            "rows": rows,
        }

        return context