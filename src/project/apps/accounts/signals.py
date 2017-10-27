from __future__ import (unicode_literals, absolute_import)

from .models import (User, Customer, Employee)
from django.dispatch import receiver
from django.db.models.signals import post_save
import logging


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

