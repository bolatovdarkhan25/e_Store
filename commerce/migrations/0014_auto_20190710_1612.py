# Generated by Django 2.2.3 on 2019-07-10 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0013_auto_20190710_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=40),
        ),
    ]
