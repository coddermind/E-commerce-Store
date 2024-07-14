from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
import cv2
from django.core.files.base import ContentFile
from io import BytesIO
import numpy as np

# Create your models here.

class Product(models.Model):
    wholesale_id=models.IntegerField(null=True,blank=True)
    name=models.CharField(max_length=200)
    price=models.IntegerField()
    price_without_discount=models.IntegerField(blank=True,null=True)

    discount_percent=models.IntegerField(blank=True,null=True)

    @property
    def discount_percent(self):
        if self.price_without_discount:
            return round((self.price_without_discount - self.price) / self.price_without_discount * 100)
        return 0

    ALL = 'all'
    MOBILE_PHONES_ACCESSORIES = 'mobile_phones_accessories'
    COMPUTERS_ACCESSORIES = 'computers_accessories'
    WEARABLE_TECHNOLOGY = 'wearable_technology'
    SMART_HOME_DEVICES = 'smart_home_devices'
    JEWELRY = 'jewelry'
    BAGS_WALLETS = 'bags_wallets'
    WATCHES = 'watches'
    HAIR_ACCESSORIES = 'hair_accessories'
    WOMEN_UNSTITCH = 'women_unstitch'
    MEN_UNSTITCH = 'men_unstitch'
    WOMEN_STITCHED = 'women_stitched'
    MEN_STITCHED = 'men_stitched'
    HEALTH_BEAUTY = 'health_beauty'
    BABY_PRODUCTS = 'baby_products'

    CATEGORY_CHOICES = [
        (ALL,'All'),
        (MOBILE_PHONES_ACCESSORIES, 'Mobile Phones & Accessories'),
        (COMPUTERS_ACCESSORIES, 'Computers & Accessories'),
        (WEARABLE_TECHNOLOGY, 'Wearable Technology'),
        (SMART_HOME_DEVICES, 'Smart Home Devices'),
        (JEWELRY, 'Jewelry'),
        (BAGS_WALLETS, 'Bags & Wallets'),
        (WATCHES, 'Watches'),
        (HAIR_ACCESSORIES, 'Hair Accessories'),
        (WOMEN_UNSTITCH, 'Women Unstitch'),
        (MEN_UNSTITCH, 'Men Unstitch'),
        (WOMEN_STITCHED, 'Women Stitched'),
        (MEN_STITCHED, 'Women Stitched'),
        (HEALTH_BEAUTY, 'Health & Beauty'),
        (BABY_PRODUCTS, 'Baby Products'),
    ]

    category_1 = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default=ALL,
    )
    category_2 = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        blank=True
    )
    category_3 = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        blank=True
    )
    category_4 = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        blank=True
    )
    category_5 = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        blank=True
    )


    date_added=models.DateTimeField(auto_now_add=True)
    description=models.TextField()

    image_1=models.ImageField(upload_to="images/")
    image_2=models.ImageField(upload_to="images/",null=True,blank=True)
    image_3=models.ImageField(upload_to="images/",null=True,blank=True)
    image_4=models.ImageField(upload_to="images/",null=True,blank=True)
    image_5=models.ImageField(upload_to="images/",null=True,blank=True)
    image_6=models.ImageField(upload_to="images/",null=True,blank=True)
    image_7=models.ImageField(upload_to="images/",null=True,blank=True)
    image_8=models.ImageField(upload_to="images/",null=True,blank=True)


    def save(self, *args, **kwargs):
        if self.image_1:
            self.image_1 = self.resize_image(self.image_1)
        if self.image_2:
            self.image_2 = self.resize_image(self.image_2)
        if self.image_3:
            self.image_3 = self.resize_image(self.image_3)
        if self.image_4:
            self.image_4 = self.resize_image(self.image_4)
        if self.image_5:
            self.image_5 = self.resize_image(self.image_5)
        if self.image_6:
            self.image_6 = self.resize_image(self.image_6)
        if self.image_7:
            self.image_7 = self.resize_image(self.image_7)
        if self.image_8:
            self.image_8 = self.resize_image(self.image_8)
        
        super(Product, self).save(*args, **kwargs)

    def resize_image(self, image_field):
        image = self.read_image(image_field)
        resized_image = cv2.resize(image, (570, 520), interpolation=cv2.INTER_CUBIC)
        return self.convert_image(resized_image, image_field.name)
    
    def read_image(self, image_field):
        image_array = np.asarray(bytearray(image_field.read()), dtype=np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    def convert_image(self, image, name):
        _, buffer = cv2.imencode('.jpg', image)
        io_buffer = BytesIO(buffer)
        return ContentFile(io_buffer.getvalue(), name=name)

    def __str__(self):
        return f"{self.id} - {self.name}"
    
    def delete(self, *args, **kwargs):
        self.delete_files()
        super().delete(*args, **kwargs)

    def delete_files(self):
        # Delete each file associated with this instance
        for field in self._meta.fields:
            if isinstance(field, models.FileField):
                file = getattr(self, field.name)
                if file and os.path.isfile(file.path):
                    os.remove(file.path)

    



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.TextField(null=True)
    product_name=models.TextField(null=True)
    product_price=models.TextField(null=True)
    product_quantity=models.TextField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_placed = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.order_placed}"
    


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=64)
    timestamp = models.DateTimeField(default=timezone.now)  # Add timestamp field


class reviews(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rating=models.IntegerField()
    name=models.CharField(max_length=150)
    email=models.EmailField()
    review=models.TextField()
