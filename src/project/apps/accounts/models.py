# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import (AbstractBaseUser, BaseUserManager)
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.conf import settings
from .utils import handle_upload_avatar
import uuid


class UserManager(BaseUserManager):

    """
    Custom user (Customer) manager
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault(str('is_staff'), False)
        extra_fields.setdefault(str('is_admin'), False)
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault(str('is_staff'), True)
        extra_fields.setdefault(str('is_admin'), True)

        if extra_fields.get(str('is_admin')) is not True:
            raise ValueError('Superuser must have is_admin=True.')

        user = self._create_user(email, password, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    """
    Customer account authentication
    """
    uid = models.UUIDField(editable=False, unique=True, verbose_name=_("Unique ID"), db_index=True)
    email = models.EmailField(verbose_name=_("Email address"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        # __unicode__ on Python 2
        return self.email

    def __unicode__(self):
        # __unicode__ on Python 3
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        pass

    def has_module_perms(self, app_label):
        pass

    def get_username(self):
        return self.email

    def clean(self):

        def generate_uid():
            return str(uuid.uuid4()).replace('-', "")

        def existed(identifier):
            user = self.objects.filter(uid=identifier).first()
            return None not in user

        def check_existed_user():
            uid = generate_uid()
            if existed(uid):
                try:
                    check_existed_user()
                except RuntimeError:
                    raise ValidationError(
                        "Unique id is existed, already retried to the maximum time, Please resubmit the form."
                    )

            self.uid = uid

        check_existed_user()

    def save(self, *args, **kwargs):
        super(self, User).save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=191, verbose_name=_("Department Name"), null=False, blank=False)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_("Created Date"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated Date"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Employee(models.Model):

    """
    Employee ORM model

    """
    uid = models.UUIDField(editable=False, unique=True, verbose_name=_("Unique ID"), db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name=_("First name"), max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=255, blank=True, null=True)
    username = models.CharField(verbose_name=_("Username"), max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=191, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(verbose_name=_("Phone number"), max_length=15, blank=True, null=True)
    fax_number = models.CharField(verbose_name=_("Fax"), max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to=handle_upload_avatar)
    bio = models.TextField(verbose_name=_("Background"), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_("Registered Date"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated Date"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    def clean(self):

        def generate_uid():
            return str(uuid.uuid4()).replace('-', "")

        def existed(identifier):
            staff = self.objects.filter(uid=identifier).first()
            return None not in staff

        def check_existed_user():
            uid = generate_uid()
            if existed(uid):
                try:
                    check_existed_user()
                except RuntimeError:
                    raise ValidationError(
                        "Unique id is existed, already retried to the maximum time, Please resubmit the form."
                    )

            self.uid = uid

        check_existed_user()

    def save(self, *args, **kwargs):
        super(self, Employee).save(*args, **kwargs)


class Customer(models.Model):

    """
    Customer account detail, this one to one relationship with customer account authentication
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name=_("First name"), max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=255, blank=True, null=True)
    username = models.CharField(verbose_name=_("Username"), max_length=255, blank=True, null=True)
    contact_number = models.CharField(verbose_name=_("Contact number"), max_length=15, blank=True, null=True)
    address = models.CharField(verbose_name=_("Current address"), max_length=255, blank=True, null=True)
    state = models.CharField(verbose_name=_("State/Origin"), max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=255, blank=True, null=True)
    country = models.CharField(verbose_name=_("Country"), max_length=255, blank=True, null=True)
    bio = models.TextField(verbose_name=_("Biology"), default="")
    date_of_birth = models.DateField(auto_created=False, verbose_name=_("Date of birth"))
    avatar = models.ImageField(upload_to=handle_upload_avatar, null=True, blank=True)

    def __str__(self):
        if self.username is not "":
            return self.username
        elif self.first_name is not "":
            return self.first_name
        elif self.last_name is not "":
            return self.last_name
        else:
            return self.user.__email

    def __unicode__(self):
        if self.username is not "":
            return self.username
        elif self.first_name is not "":
            return self.first_name
        elif self.last_name is not "":
            return self.last_name
        else:
            return self.user.__email

    def get_full_name(self):
        if self.last_name != "" and self.first_name != "":
            return self.first_name + " " + self.last_name
        elif self.username != "":
            return self.username
        else:
            return self.user.__email

    def get_avatar_picture(self, **kwargs):
        css_class = kwargs[str('cls')] if 'cls' in kwargs else ""
        if self.avatar and hasattr(self.avatar, 'url'):
            if 'square' in kwargs and kwargs[str('square')] is True:
                return format_html(
                    '<img src="{0}" width="90px" height="90px" class="img-responsive avatar_profile {1}">'.format(
                        self.avatar.url, css_class
                    )
                )
            else:
                return format_html(
                    '<img src="{0}" class="img-responsive avatar_profile {1}">'.format(
                        self.avatar.url, css_class
                    )
                )
        else:
            return format_html(
                '<img src="{0}" class="img-responsive avatar_profile {1}">'.format(
                    settings.STATIC_URL + "accounts/img/avatar/default_avatar.png", css_class
                )
            )



