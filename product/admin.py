from typing import List

from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.contrib.filters.admin import RangeNumericFilter
from unfold.contrib.import_export.forms import ImportForm, ExportForm
from unfold.decorators import display
from product.models import Product, Category, Color, Size
from product.sites import custom_admin_site






class CategoryTabular(StackedInline):
    model = Product
    tab = True
    can_delete = True
    extra = 1

@admin.register(Product,site=custom_admin_site)
class ProductAdmin(ModelAdmin):
    model = Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['id','name','category','color','size','get_price','stock']
    search_fields = ['name','category__name','color__name','size__name']
    list_per_page = 10
    list_display_links = ['id','name']
    list_filter = [('stock',RangeNumericFilter)]
    list_filter_submit = True
    def get_price(self,obj):
        return f"{int(obj.price):,}".replace(",", " ") + " so'm"

    get_price.short_description = 'Narxi'




@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['id','parent_category','name','description']
    list_display_links = ['id','parent_category','name']
    inlines = [CategoryTabular]
    @display(description="Ota Kategoriya")
    def parent_category(self,obj):
        return obj.parent.name if obj.parent else ''

@admin.register(Color)
class ColorAdmin(ModelAdmin):
    list_display = ['id','name']

@admin.register(Size)
class SizeAdmin(ModelAdmin):
    list_display = ['id','name']