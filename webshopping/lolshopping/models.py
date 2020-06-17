from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name = 'email', max_length = 60, unique=True)
    username = models.CharField(max_length = 30, unique=True)




# Create your models here.
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
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

class UserInfo(models.Model):
    uName = models.CharField(max_length=50)
    uEmail = models.CharField(max_length=50)
    uPhone = models.CharField(max_length=50)
    uAddress1 = models.CharField(max_length=50)
    uAddress2 = models.CharField(max_length=50)
    uCity = models.CharField(max_length=50)
    uState = models.CharField(max_length=50)
    uZip = models.CharField(max_length=50)
    uCardType = models.CharField(max_length=50)
    uNameOnCard = models.CharField(max_length=50)
    uCardNumber = models.CharField(max_length=50)
    uExpiration_date = models.CharField(max_length=50)
    uCvc_number = models.CharField(max_length=50)
    uDelivery_option = models.CharField(max_length=50)

