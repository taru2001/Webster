from django.db import models

# Create your models here.

class User(models.Model):
    name_id=models.AutoField
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    mobile=models.IntegerField()
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=25)

    def __str__(self):
       return self.name 
