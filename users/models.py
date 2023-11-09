import random

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager, send_mail


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True, 
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )
        if not extra_fields.get('no_password'):
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            elif phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwqyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))
        
        return self._create_user(username, phone_number, email, password, False, False, **extra_fields)

    def create_superuser(self, username, phone_number=None, email=None, password=None, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and _ only."
        ),
        validators=[
            validators.RegexValidator(
                r'[A-Za-z0-9_]{3,15}',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers and _ character.'),
                'invalid'
            )
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        }
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(
        _("email address"), unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(
        _('phone number'),
        unique=True,
        null=True,
        blank=True,
        validators=[
            validators.RegexValidator(
                r'^989([0-3]|9)\d{8}$',
                _('Enter a valid phone number'),
                'invalid'
            )
        ],
        error_messages={
            "unique": _("A user whith this phone number already exists.")
        }
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number"]

    class Meta:
        db_table = 'users'
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_loggedin_user(self):
        """
        Return True if user has actually logged in with valid credentials
        """
        return self.phone_number is not None or self.email is not None
    
    def save(self, *args, **kwargs):
        """
        Handle blank email for not conflicting unique field
        """
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    nickname = models.CharField(_('nick name'), max_length=150, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='users/', blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    gender = models.BooleanField(
        _('gender'), 
        null=True, 
        help_text="male is True and Female is False. null is unset."
    )
    province = models.ForeignKey('Province', verbose_name=_('province'), null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_first_name(self):
        return self.user.first_name
    
    @property
    def get_last_name(self):
        return self.user.last_name
    
    def nick_name(self):
        return self.nick_name if self.nick_name else self.user.username
    
    def __str__(self):
        return self.user.username


class Device(models.Model):
    WEB = 1
    ANDROID = 2
    IOS = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (ANDROID, 'android'),
        (IOS, 'ios'),
    )

    user = models.ForeignKey('User', related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_('Device UUID'), null=True)
    # notify_token = models.CharField(
    #     _('Notification token'),
    #     max_lenght=200,
    #     blank=True,
    #     validators=[
    #         validators.RegexValidator(r'([A-Z][a-z][0-9])\w+',
    #         _('Notify token is not valid.'),
    #         'invalid'
    #         )
    #     ]
    # )
    last_login = models.DateTimeField(_('last login'), null=True)
    device_type = models.PositiveSmallIntegerField(
        _('device type'),
        choices=DEVICE_TYPE_CHOICES,
        default=WEB
    )
    device_os = models.CharField(_('device os'), max_length=20, blank=True)
    device_model = models.CharField(_('device model'), max_length=50, blank=True)
    app_version = models.CharField(_('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(_('created_time'), auto_now_add=True)

    class Meta:
        db_table = 'user_devices'
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        unique_together = ('user', 'device_uuid')


class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name