# Generated by Django 3.0.7 on 2020-06-22 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lolshopping', '0002_champions_customer_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='hash_value',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
