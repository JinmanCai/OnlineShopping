from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os
import hashlib

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name = 'email', max_length = 60, unique=True)
    username = models.CharField(max_length = 30, unique=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hash_value = models.CharField(max_length = 100, null=True)
    salt = models.CharField(max_length = 100, null=True)
    new_salt = models.CharField(max_length = 100, null=True)
    new_hash_value = models.CharField(max_length = 100, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email


    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return True

    def save(self, *args, **kwargs):
        try:
            self.new_salt = os.urandom(32)
            super().save(*args, **kwargs)
        except IntegrityError:
            self.save(*args, **kwargs)





class Champions(models.Model):

    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places = 0, max_digits=2)
    picture = models.ImageField(upload_to='champic/')
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url

class Customer(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True,null=True)
    complete = models.BooleanField(default=False,null=True,blank=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Champions,on_delete=models.SET_NULL, blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True,null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
