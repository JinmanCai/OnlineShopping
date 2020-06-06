from django.db import models

# Create your models here.
class Champions(models.Model):

    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places = 0, max_digits=2)
    picture = models.ImageField(upload_to='champic/')
    def __str__(self):
        return self.name


