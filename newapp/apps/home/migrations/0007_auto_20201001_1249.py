# Generated by Django 3.1 on 2020-10-01 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20201001_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.ImageField(default='', upload_to='home/images'),
        ),
    ]
