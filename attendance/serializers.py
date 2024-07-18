from rest_framework import serializers
from attendance.models import *



class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id","full_name","username","email","role"]
        
class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'