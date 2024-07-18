from django.db import models
from .employee import Employee

class StaffRoster(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    weekly_off = models.TextField(null=True,blank=True)


    class Meta:
        db_table = "staff_roster"