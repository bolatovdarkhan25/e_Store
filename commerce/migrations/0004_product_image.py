# Generated by Django 2.2.3 on 2019-07-09 05:50

import commerce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0003_auto_20190709_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to=commerce.models.image_folder),
        ),
    ]
