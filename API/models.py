import uuid

from django.contrib.auth.models import AbstractUser,Group
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

from API.Validators import validate_lowercase


class UserAccount(AbstractUser):
    GENDER_CHOICES = [
        ('Customer', 'Customer'),
        ('Trader', 'Trader'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_lowercase]


    )
    email = models.EmailField(
        default=None, blank=True,
        verbose_name='email address',
        max_length=255,
        unique=True,
        validators=[EmailValidator(message='Enter a valid email address.')]
    )
    user_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type=models.CharField(max_length=60, choices=GENDER_CHOICES,default=None,blank=True)
    phone_number= PhoneNumberField(default=None,blank=True)
    otp_enabled = models.BooleanField(default=False)
    otp_base32 = models.CharField(max_length=255, null=True,blank=True)
    otp_auth_url = models.CharField(max_length=255, null=True,blank=True)

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
    manager=models.ForeignKey(UserAccount,on_delete=models.CASCADE, limit_choices_to={'type': 'Trader'},)
    store_name=models.CharField(max_length=500,blank=True)
    longitude=models.FloatField(null=False,blank=True)
    latitude=models.FloatField(null=False,blank=True)
    is_available=models.BooleanField(null=False,blank=True,default=True)
    adress=models.CharField(max_length=500,null=False,blank=True,default='-')



class Comment(models.Model):
    comment_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rate=models.PositiveIntegerField(default=0)
    comment_text=models.TextField(null=True,blank=True)
    by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, limit_choices_to={'type': 'Customer'})
    at= models.DateTimeField(auto_now=True)
