from django.db import models
from django.contrib.auth.models import User

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

