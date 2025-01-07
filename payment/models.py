from django.db import models

from order.models import Order


# Create your models here.
class Payment(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='payment')
    amount = models.DecimalField(max_digits=16,decimal_places=2,verbose_name="To'lov summasi",default=0.00)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} To'lovi: {self.amount}"
    class Meta:
        db_table = 'payment'
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"