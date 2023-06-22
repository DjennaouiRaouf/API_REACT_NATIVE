import uuid

from django.contrib.auth.models import AbstractUser,Group
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class UserAccount(AbstractUser):
    GENDER_CHOICES = [
        ('Customer', 'Customer'),
        ('Trader', 'Trader'),
    ]
    user_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type=models.CharField(max_length=60, choices=GENDER_CHOICES)
    phone_number= PhoneNumberField()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'




class GroupUser(Group):
    group_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

class Store(models.Model):
    store_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manager=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    store_name=models.CharField(max_length=500,blank=True)
    longitude=models.FloatField(null=False,blank=True)
    latitude=models.FloatField(null=False,blank=True)


