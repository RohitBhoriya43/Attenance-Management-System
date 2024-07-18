from django.db import models
from django.contrib.auth.models import AbstractUser
from attendance.choices import *
import uuid

def generate_uuid():
    return uuid.uuid4().hex

class Employee(AbstractUser):
    id = models.CharField(max_length=200,primary_key=True,editable=False, default=f"employee_{generate_uuid()}")
    full_name = models.CharField(max_length=200,null=True)
    username = models.CharField(max_length=200,unique=True,default= f"{generate_uuid()}")
    email = models.CharField(max_length=200,null=True)
    role = models.CharField(max_length=200,choices=Role.choices,default= Role.Staff)

    def __str__(self):
        return self.username
    class Meta:
        db_table = "employee"