from django.db import models

# Create your models here.

from django.db import models

class CityChoice(models.TextChoices):
    ANDIJON = 'Andijon', 'Andijon'
    BUXORO = 'Buxoro', 'Buxoro'
    FARGONA = 'Farg‘ona', 'Farg‘ona'
    JIZZAX = 'Jizzax', 'Jizzax'
    XORAZM = 'Xorazm', 'Xorazm'
    NAMANGAN = 'Namangan', 'Namangan'
    NAVOIY = 'Navoiy', 'Navoiy'
    QASHQADARYO = 'Qashqadaryo', 'Qashqadaryo'
    QORAQALPOGISTON = 'Qoraqalpog‘iston', 'Qoraqalpog‘iston'
    SAMARQAND = 'Samarqand', 'Samarqand'
    SIRDARYO = 'Sirdaryo', 'Sirdaryo'
    SURXONDARYO = 'Surxondaryo', 'Surxondaryo'
    TOSHKENT = 'Toshkent', 'Toshkent'
    TOSHKENT_SHAHAR = 'Toshkent shahar', 'Toshkent shahar'

class Customer(models.Model):
    first_name = models.CharField(max_length=40,verbose_name="Ismi")
    last_name = models.CharField(max_length=40,verbose_name="Familiyasi",null=True,blank=True)
    phone_number = models.CharField(max_length=20,verbose_name="Telefon raqami",unique=True)
    birth_date = models.DateField(verbose_name="Tug'ilgan yili",null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        if self.last_name:
           return f"{self.first_name} {self.last_name}"
        return self.first_name

    def __str__(self):
        return f"{self.full_name()} - {self.phone_number}"

    class Meta:
        verbose_name = 'Mijoz'
        verbose_name_plural = 'Mijozlar'

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses",verbose_name='Mijoz')
    city = models.CharField(max_length=100,verbose_name="Viloyat",choices=CityChoice.choices)
    state = models.CharField(max_length=100,verbose_name='Shahar')
    address_line = models.CharField(max_length=255,verbose_name="Manzil")
    postal_code = models.CharField(max_length=20,null=True,blank=True,verbose_name='Pochta indeksi')
    phone = models.CharField(max_length=15, blank=True, null=True,verbose_name="Telefon raqam(qo'shimcha)")  # Qo‘shimcha telefon
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer}, {self.city}, {self.state}, {self.address_line}"

    class Meta:
        db_table = 'address'
        verbose_name = 'Manzil'
        verbose_name_plural = 'Manzillar'
        ordering = ['-created_at']