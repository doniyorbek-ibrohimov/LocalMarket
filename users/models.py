from django.db import models
from django.contrib.auth.models import AbstractUser


CUSTOMER, ADMIN = ('customer', 'admin')

class User(AbstractUser):
    USER_ROLES=(
        (CUSTOMER, CUSTOMER),
        (ADMIN, ADMIN),
    )
    phone = models.CharField(max_length=31, blank=True, null=True)
    role = models.CharField(max_length=31, choices=USER_ROLES, default=CUSTOMER)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

