# -*- encoding: utf-8 -*-
from django.db import models
import re
import uuid

from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth import models as auth_models
from django import forms
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

class UserManager(BaseUserManager):
    """
        Creates and saves a User with the given email and password.
    """

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_(
                                    'Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'),
                                                              _('invalid'))
                                ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=255, unique=True, null=True, default="your@email.com")
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    dob = models.DateField(_('date of birth'), blank=True, null=True)

    ip = models.CharField(_('IP address'), max_length=40, default="127.0.0.1")
    lastlogin = models.BigIntegerField(_('Last login'), default=False)
    x = models.FloatField(_('X coord'), default="0")
    y = models.FloatField(_('Y coord'), default="0")
    z = models.FloatField(_('Z coord'), default="0")
    world = models.CharField(_('World name'), max_length=255, null=True, default="survival")
    isLogged = models.SmallIntegerField(_('Is logged user'), default="0")
    realname = models.CharField(_('Realname'), max_length=255, default="MOB Player")


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    ## define the user manager class for User
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def has_email(self):
        return self.email and self.email != "your@email.com"

    def get_email(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], fail_silently=False)

    def set_activation_data(self, activation_key, key_expires):
        """
        Set activation data when register initially
        """
        self.activation_key = activation_key
        self.key_expires = key_expires
