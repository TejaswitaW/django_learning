""" Each model is a python class"""
import random
import os
from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.urls import reverse
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


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def features(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        query_set = self.get_queryset().filter(id=id)
        if query_set.count() == 1:
            # gives individual object
            return query_set.first()
        return None


class Product(models.Model):
    """This is design of our model"""
    title = models.CharField(max_length=120)
    # slug = models.SlugField(blank=True,null=True)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    # image = models.FileField(
    #     upload_to=upload_image_path, null=True, blank=True)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
