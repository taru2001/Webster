# Generated by Django 3.1 on 2020-10-15 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paytm', '0003_order_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]