# Generated by Django 2.2.3 on 2019-07-10 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0010_auto_20190710_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_total_price',
            field=models.DecimalField(decimal_places=2, max_digits=40),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='item_total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=30),
        ),
    ]
