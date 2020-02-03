# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
# Create your models here.
from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from LMS.choices import *
import uuid

class User(models.Model):
    def create_user(
            self,
            username,
            email,
            occupation,
            location,
            first_name,
            address,
            phone_number,
            account_type,
            password,
            is_mentor,

            **kwargs
    ):
        msg = 'Account must have a valid %s.'
        if not email:
             raise ValueError(msg % 'email address')


        account = self.model(
            username=username,
            email=email,
            occupation=occupation,
            location=location,
            first_name=first_name,
            address=address,
            phone_number=phone_number,
            password=password,
            is_mentor=is_mentor,
            account_type=account_type,

        )
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(
            self,
            username,
            email,
            occupation,
            location,
            first_name,
            address,
            phone_number,
            password,
            is_mentor,
            **kwargs):
        account = self.create_user(
        username,
        email,
        occupation,
        location,
        first_name,
        address,
        phone_number,
        password,
        is_mentor,
        )
        account.is_admin =True
        account.is_superuser = True
        account.is_staff = True
        account.save(using=self._db)
        return account
        
class Account(AbstractBaseUser,PermissionsMixin):
    # TODO: Add created_at and modified_at fields for this model.
    username = models.CharField(max_length=40,unique=True,blank=True,null=True)
    first_name = models.CharField(max_length=40,blank=True,null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    address = models.CharField(max_length=350,blank=True,null=True)
    phone_number = models.CharField(
            max_length=10,
            unique=True,
            blank=True,null=True,
            help_text="Enter the phone number WITHOUT country code"
        )
    account_types=(('Employer','Employer'),('mentor','mentor'))
    account_type = models.CharField(max_length=30,choices=account_types,null=True, blank=True)

    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    is_staff = models.BooleanField(default=False)
    occupation = models.IntegerField(choices=OCCUPATION_CHOICES, default=1)
    location = models.CharField(
            max_length=50,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default = True)
    is_verified = models.BooleanField(default=False)

    #mentor
    technologies=models.CharField(max_length=100,blank=True,null=True)
    experience=models.CharField(max_length=100,blank=True,null=True)
    #employer
    organisation=models.CharField(max_length=100,blank=True,null=True)
    position=models.CharField(max_length=100,blank=True,null=True)
    acc_key= models.CharField(unique=True,max_length=100,blank=True,null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [

            'occupation',
            'location',
            'first_name',
            'address',
            'username'
    ]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return '{0} ({1})'.format(self.username, self.phone_number)

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def set_email(self, email):
        self.email = email

    def set_phone_number(self,phone_number):
        self.phone_number=phone_number




class Image(models.Model):
    account_image = models.ForeignKey(Account,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image',verbose_name='image',)

# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'documents/{0}/{1}'.format(instance.user.username, filename)
# class Document(models.Model):
#     user=models.ForeignKey(Account, blank=True, null=True)
#     description = models.CharField(max_length=255, blank=True)
#     document = models.FileField(upload_to=user_directory_path)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

class PasswordReset(models.Model):
   user = models.ForeignKey(Account,on_delete=models.CASCADE)
   key = models.UUIDField(default=uuid.uuid4 , editable=False , unique=True)
   submited_key = models.CharField(max_length=70)
   timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

   def __str__ (self):
       return self.user.username
