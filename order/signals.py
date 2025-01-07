from decimal import Decimal

from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from payment.models import Payment
from product.models import Product
from .models import OrderItem, Order, StatusChoice


@receiver(pre_save, sender=OrderItem)
def update_stock_on_order(sender, instance, **kwargs):
    if instance.pk:  # Mavjud buyurtma tahrirlanmoqda
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.quantity != instance.quantity:
            product = instance.product
            order = instance.order
            product.stock += old_instance.quantity  # Eski miqdorni qo'shish
            product.stock -= instance.quantity  # Yangi miqdorni ayirish
            product.save()
            order.total_price=Decimal(order.total_price)-old_instance.total_price()
            order.total_price=Decimal(order.total_price)+instance.total_price()
            order.save()
    else:  # Yangi buyurtma yaratilmoqda
        product = instance.product
        if product.stock >= instance.quantity:
            product.stock -= instance.quantity
            product.save()
            order = instance.order
            order.total_price=Decimal(order.total_price)+instance.total_price()
            order.save()
        else:
            raise ValueError("Yetarli zaxira yo'q!")

@receiver(pre_save,sender=Order)
def update_stock_on_order(sender,instance,**kwargs):
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if instance.status==StatusChoice.CANCELED:
            for order_item in instance.items.all():
                product = order_item.product
                product.stock += order_item.quantity
                product.save()
        if  not old_instance.is_paid and instance.is_paid:
            amount = 0
            for order_item in instance.items.all():
                amount += order_item.total_price()
            amount-=instance.discount
            Payment.objects.create(order=instance,amount=amount)

# @receiver(post_save,sender=Order)
# def update_total_price(sender,instance,created,**kwargs):
#     if created:
#         if instance.items.exists():
#             amount = 0
#             for order_item in instance.items.all():
#                 amount += order_item.total_price()
#             instance.total_price = amount
#             instance.save()
