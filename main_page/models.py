from django.db import models
from django.core.validators import RegexValidator
import uuid
import os

# Create your models here.
class DishCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    position = models.PositiveSmallIntegerField(unique=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}: {self.position}"

    class Meta:
        ordering = ("position", )

class Dish(models.Model):
    def get_file_name(self, filename: str):
        ext = filename.strip().split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('images/dishes', filename)

    name = models.CharField(max_length=50, unique=True)
    position = models.PositiveSmallIntegerField()
    is_visible = models.BooleanField(default=True)
    category = models.ForeignKey(DishCategory, on_delete=models.CASCADE)
    is_special = models.BooleanField(default=False)
    desc = models.TextField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    ingredients = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=get_file_name)

    class Meta:
        ordering = ("position", )

    def __str__(self):
        return f"{self.name}"

class Gallery(models.Model):
    def get_file_name(self, filename: str):
        ext = filename.strip().split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('images/gallery', filename)

    photo = models.ImageField(upload_to=get_file_name)
    desc = models.CharField(max_length=100, blank=True)
    is_visible = models.BooleanField(default=True)

class UserReservation(models.Model):
    phone_validator = RegexValidator(regex=r'^\+?(38)?0?\d{2}[- ]?(\d[- ]?){7}$', message='Phone number should be in +38 xxx xxx xx xx format')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, validators=[])
    persons = models.PositiveSmallIntegerField()
    message = models.TextField(max_length=250, blank=True)
    date = models.DateField(auto_now_add=True)
    manage_date_processed = models.DateField(auto_now=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ("-date", )

    def __str__(self):
        return f"{self.name} {self.phone}: {self.message[:20]}"