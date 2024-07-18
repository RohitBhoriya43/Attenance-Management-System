from django.db import models

from .roster_staff import StaffRoster
from .employee import Employee
from django.utils import timezone
from .shift import Shift

class Attendance(models.Model):
    staff = models.ForeignKey(StaffRoster,on_delete=models.CASCADE,null=True)
    shift = models.ForeignKey(Shift,on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.TextField(null=True)

    class Meta:
        db_table = "attendance"