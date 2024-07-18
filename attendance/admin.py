# attendance/admin.py

from django.contrib import admin, messages
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from attendance.models import *



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id',"full_name","username","role")
    
    

    def save_model(self, request, obj, form, change):
        try:
            if obj.password and not obj.password.startswith('pbkdf2_sha256$'):
                obj.password = make_password(obj.password)
            if Employee.objects.filter(email=obj.email).exists():
                raise ValidationError("A user with that email already exists.")
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            for message in e.messages:
                messages.error(request, message)

@admin.register(StaffRoster)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('employee',)

    def save_model(self, request, obj, form, change):
        try:
            if obj.employee.role != 'staff':
                raise ValidationError("Only users with the 'staff' role can be added as staff members.")
            if StaffRoster.objects.filter(employee__id = obj.employee.id).exists():
                raise ValidationError("This employee id or username is already exists")
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            for message in e.messages:
                messages.error(request, message)

# @admin.register(Shift)
# class ShiftAdmin(admin.ModelAdmin):
#     list_display = ('staff', 'day_of_week', 'start_time', 'end_time')
#     list_filter = ('day_of_week',)
#     search_fields = ('staff__user__username', 'staff__user__email')

# @admin.register(Attendance)
# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ('staff', 'timestamp', 'image')
#     list_filter = ('timestamp',)
#     search_fields = ('staff__user__username', 'staff__user__email')
