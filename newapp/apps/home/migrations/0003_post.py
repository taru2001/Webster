# Generated by Django 3.1 on 2020-10-01 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200930_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.CharField(max_length=40)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('video', models.FileField(upload_to='userVideos')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user')),
            ],
        ),
    ]
