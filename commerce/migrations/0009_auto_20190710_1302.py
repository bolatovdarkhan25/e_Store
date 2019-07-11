# Generated by Django 2.2.3 on 2019-07-10 07:02

import commerce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0008_cart_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart_Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=10)),
                ('slug', models.SlugField(blank=True, default='', max_length=10)),
                ('image', models.ImageField(default='', upload_to=commerce.models.image_folder)),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='image',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='slug',
        ),
    ]