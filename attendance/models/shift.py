from django.db import models
from .employee import Employee
from .roster_staff import StaffRoster
from attendance.choices import *

class Shift(models.Model):
    staff = models.ForeignKey(StaffRoster,on_delete=models.CASCADE,null=True)
    week_id = models.CharField(max_length=200,null=True,blank=True)
    day_of_week = models.CharField(max_length=200,choices=DayOfWeek.choices,default=DayOfWeek.Monday)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    class Meta:
        db_table = "shift"