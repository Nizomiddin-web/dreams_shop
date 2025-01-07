from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200,verbose_name="Kategoriya nomi")
    description = models.CharField(max_length=500,verbose_name="Kategoriya tavsifi",null=True,blank=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='Categories/',null=True,blank=True,verbose_name="Rasmi")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200,verbose_name='nomi',unique=True)
    hex_value = models.CharField(max_length=200,null=True,blank=True,verbose_name="rang kodi")

    class Meta:
        db_table = 'color'
        verbose_name = 'Rang'
        verbose_name_plural = 'Ranglar'
        ordering = ['-created_at']

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=200,verbose_name="nomi")

    def __str__(self):
        return self.name

class Product(models.Model,):
    name = models.CharField(max_length=200,verbose_name='nomi')
    description = models.TextField(null=True,blank=True,verbose_name='hususiyatlari')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='Kategoriyasi')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='rangi')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="o'lchami")
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="narxi")
    stock = models.PositiveIntegerField(verbose_name='soni',default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True,verbose_name='rasmi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_price(self):
        return f"{int(self.price):,}".replace(",", " ") + " so'm"

    class Meta:
        db_table = 'product'
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'
        ordering = ['-created_at']
    def __str__(self):
        color_name = self.color.name if self.color else ''
        size_name = self.size.name if self.size else ''
        return f"{self.name} {color_name} {size_name}"
