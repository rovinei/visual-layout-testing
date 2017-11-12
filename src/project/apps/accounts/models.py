# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.conf import settings
from .utils import handle_upload_avatar
from django.dispatch import receiver
from django.db.models.signals import post_save
import logging


class Employee(models.Model):

    """
    Employee ORM model

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name=_("First name"), max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=255, blank=True, null=True)
    username = models.CharField(verbose_name=_("Username"), max_length=255, blank=True, null=True)
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

    def __avatar_img__(self):
        if hasattr(self.avatar, 'url'):
            return format_html('<img height="90px" src="{}" crossorigon="annonymous" />'.format(self.avatar.url))
        else:
            return format_html('<img height="90px" src="no-image.jpg" crossorigon="annonymous" />')


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


@receiver(post_save, sender=User)
def create_customer_info(sender, **kwargs):

    """
    Create blank customer information record after received post_save signal
    from Customer registered model

    :param sender: which model was being sent
    :param kwargs: keyword argument of model instance
    :return: void
    """

    if isinstance(sender, Customer):
        if 'created' in kwargs and 'instance' in kwargs:
            user = kwargs[str('instance')]
            if hasattr(user, 'is_staff') and user.is_staff is True:
                employee = Employee.objects.create(user=user)
                if employee:
                    logging.info("Successfully created employee info record")
            else:
                customer = Customer.objects.create(user=user)
            if customer:
                logging.info("Successfully created customer info record")
