""" Each model is a python class"""
import random
import os
from django.db import models

# Create your models here.


def get_filename_ext(filepath):
    """This function returns file name and its extention"""
    # if we have passed file path
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    """Creats new file name"""
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 2582359728)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(
        new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename,
                                                             final_filename=final_filename)


class ProductManager(models.Manager):
    def get_by_id(self, id):
        return self.get_queryset().filter(id=id)


class Product(models.Model):
    """This is design of our model"""
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    # image = models.FileField(
    #     upload_to=upload_image_path, null=True, blank=True)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    objects = ProductManager()

    def __str__(self):
        return self.title
