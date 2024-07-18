from .imports import *


class ViewAttendance(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsManagerPermission,)

    def get(self,request,*args,**kwargs):
        try:
            employee_id = request.query_params.get('employee_id')
            current_day = check_str_true_false(request.query_params.get('current_day'))
            current_week = check_str_true_false(request.query_params.get('current_week'))

            if employee_id:
                filter_data=self.check_current_day_current_week({"staff__employee__id": employee_id},current_day,current_week)
                attendance_data = self.find_out_attendance_obj(filter_data)
                attendance_data= {
                    "employee_id":attendance_data.first().staff.employee.id,
                    "full_name":attendance_data.first().staff.employee.full_name,
                    "attendances":attendance_data.values(week_id=F("shift__week_id"),attendance_timestamp=F("timestamp"),day_of_week=F("shift__day_of_week"),attendance_image=F("image"))
                }
            else:
                roster_staff = StaffRoster.objects.all()
                attendance_data=self.set_all_attendance_data(roster_staff,current_day,current_week)

            return Response(attendance_data,status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)
        
    
    def find_out_attendance_obj(self,filter_data):
        attendance_data = Attendance.objects.filter(**filter_data)
        return attendance_data
    
    def check_current_day_current_week(self,filter_data,current_day,current_week):
        if current_day and not current_week:
            filter_data.update({"shift__week_id":findOutCurrentWeekId(),"shift__day_of_week":findDayForToday()})
        elif current_week and not current_day:
            filter_data.update({"shift__week_id":findOutCurrentWeekId()})
        else:
            filter_data.update({"shift__week_id":findOutCurrentWeekId()})
        return filter_data
    
    def set_all_attendance_data(self,roster_staff,current_day,current_week):
        attendance_list = []
        for staff in roster_staff:
            filter_data = self.check_current_day_current_week({"staff":staff},current_day,current_week)
            attendance_data = self.find_out_attendance_obj(filter_data)
            data = {
                "employee_id":staff.employee.id,
                "full_name":staff.employee.full_name,
                "roster_id":staff.id,
                "attendances": attendance_data.values(week_id=F("shift__week_id"),attendance_timestamp=F("timestamp"),day_of_week=F("shift__day_of_week"),attendance_image=F("image"))
            }
            # print("data",data)
            attendance_list.append(data)
        
        return attendance_list