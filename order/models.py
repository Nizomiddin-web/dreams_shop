from django.db import models

from customer.models import Address, Customer
from product.models import Product

class StatusChoice(models.TextChoices):
    GET_TOMORROW = 'get_tomorrow', "🤥 Keyin oladi"
    HOLD = 'hold', "🗳 Zakazga"
    PENDING = 'pending',"📦 Qabul qilindi"
    READY_DELIVERY = 'ready_delivery',"🛍 Dastavkaga Tayyor"
    SHIPPED = 'shipped',"🚚 Yetkazilmoqda (Yo'lda)"
    DELIVERED = 'delivered',"Yetkazib berildi✅"
    CANCELED = 'canceled',"❌ Bekor qilindi"

class PaymentMethodChoice(models.TextChoices):
    CASH = 'cash',"💵 Naqt"
    CARD = "card","💳 Kartaga"
    MAIL = "mail", "📨 Pochta orqali"

# Create your models here.TailwindBaseForm
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.CASCADE,related_name="addresses")
    description = models.CharField(max_length=300,null=True,blank=True,verbose_name="Tavsif")
    payment_method = models.CharField(max_length=50,null=True,blank=True,choices=PaymentMethodChoice.choices,verbose_name="To'lov turi")
    discount = models.DecimalField(decimal_places=2,max_digits=10,verbose_name="Chegirma summasi",default=0.00)
    prepayment = models.DecimalField(decimal_places=2,max_digits=10,verbose_name="Oldindan to'lov summasi",default=0.00)
    image = models.ImageField(upload_to="orders/",verbose_name="Rasm",null=True,blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoice.choices,
        default=StatusChoice.PENDING
    )
    total_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Jami to'lov",
                                      default=0.00)
    is_paid = models.BooleanField(verbose_name="To'lov qildimi?",default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.first_name}"

    class Meta:
        db_table = 'order'
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="items")
    quantity = models.PositiveIntegerField(default=0,verbose_name="Buyurtma soni")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        return self.quantity * self.product.price

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Buyurtma mahsuloti'
        verbose_name_plural = 'Buyurtma mahsulotlari'
        ordering = ['-created_at']
