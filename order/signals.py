from decimal import Decimal

import requests
from django.db import transaction
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

# TELEGRAM_BOT_TOKEN = '5209842887:AAHGMkYY2ye6XaFReu9Ex8hNlwKrF7B9yLQ'
TELEGRAM_BOT_TOKEN = '57977019764:AAHN1vajZMqHHIerVleKPjlROGO8EYDsMTc'
# TELEGRAM_CHAT_ID = '1987938749'
TELEGRAM_CHAT_ID = '-1004722321542'
@receiver(post_save,sender=Order)
def update_total_price(sender,instance,created,**kwargs):
    if created:
        def notify():
                try:
                    payment_method_display = instance.get_payment_method_display()
                    status_display = instance.get_status_display()
                    product = ""
                    total_price = f"{int(instance.total_price):,}".replace(","," ") + " so'm"
                    for item in instance.items.all():
                        product+=f"{item.product.name},"
                    message = (
                        f"<b>Buyurtma</b>\n\n"
                        f"<b>#ID:</b>{instance.id}\n"
                        f"<b>👤Mijoz :</b> {instance.customer.full_name()}\n"
                        f"<b>📞Telefon raqam :</b> {instance.customer.phone_number}\n"
                        f"<b>💠Address :</b> {instance.address.city}, {instance.address.address_line}\n"
                        f"<b>📦Mahsulotlar :</b> {product}\n"
                        f"<b>📊Status :</b> {status_display}\n"
                        f"<b>To'lov turi :</b> {payment_method_display}\n"
                        f"<b>💰Jami :</b> {total_price}\n"
                        f"<b>To'lov qildimi? :</b> {"Ha" if instance.is_paid else "Yo'q"}"
                    )
                    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message,"parse_mode":"HTML"}

                    requests.post(url, data=data)
                except Exception as e:
                    print(f"Telegramga xabar yuborishda xatolik: {e}")

        transaction.on_commit(notify)

