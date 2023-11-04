from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True)    
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='categories/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)


    class __Meta__():
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True)    
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='products/')
    categories = models.ManyToManyField('Category', verbose_name=_('categories'), blank=True)
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)


    class __Meta__():
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class File(models.Model):
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True)    
    file = models.FileField(_('file'), blank=True, upload_to='files/%Y/%m/%d/')
    product = models.ForeignKey('Product', verbose_name=_('product'), blank=True, null=True, on_delete=models.CASCADE)
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)


    class __Meta__():
        db_table = 'files'
        verbose_name = 'File'
        verbose_name_plural = 'Files'
