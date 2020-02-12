"""MODEL for product ie. item"""
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
from djmoney.models.fields import MoneyField
from django_extensions.db.fields import AutoSlugField
from hitcount.models import HitCount
from PIL import Image

from .options import CATEGORY_CHOICES, CONDITION_CHOICES, SUB_CATEGORY_CHOICES


class Category(models.Model):
    """ Category class"""
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    slug = AutoSlugField(populate_from=['name'])

    class Meta:
        """additional properties class"""
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.get_name_display()


class SubCategory(models.Model):
    """ SubCategory class"""
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subname = models.CharField(max_length=100, choices=SUB_CATEGORY_CHOICES)
    slug = AutoSlugField(populate_from=['subname'])

    class Meta:
        """additional properties class"""
        # ordering = ('subname',)
        verbose_name = 'Sub_Category'
        verbose_name_plural = 'Sub_Categories'

    def __str__(self):
        # return self.subname returns the non human readable tuple
        return self.get_subname_display()  # returns human readable tuple


class Item(models.Model):
    """ Item class"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    price = MoneyField(decimal_places=2, max_digits=10, default_currency='NPR')
    content = models.TextField()
    image = models.ImageField(upload_to='item_pics/')  # setting image
    condition = models.CharField(
        max_length=100, null=True, blank=True, choices=CONDITION_CHOICES)

    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    slug = AutoSlugField(populate_from=['title', 'author'])

    if image:
        def save(self, *args, **kwargs):
            # accessing parent class save function
            super(Item, self).save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)  # overriding previous image

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'slug': self.slug})
