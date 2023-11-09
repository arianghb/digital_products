from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.validators import validate_sku

class Package(models.Model):
    sku = models.CharField(_('stuck kipping unit'), max_length=20, validators=[validate_sku], db_index=True)
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='packages/', blank=True)
    price = models.PositiveBigIntegerField(_('price'))
    is_enable = models.BooleanField(_('is enable'), default=True)
    duration = models.DurationField(_('duration'), blank=True, null=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    class Meta:
        db_table = 'packages'
        verbose_name = _('Package')
        verbose_name_plural = _('Packages')

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    package = models.ForeignKey('Package', on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    expire_time = models.DateTimeField(_('expire time'))

    class Meta:
        db_table = 'subscriptions'
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')