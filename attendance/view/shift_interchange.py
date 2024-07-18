from .imports import *

class ShiftInterchange(APIView):
    authentication_classes=(JWTAuthentication,)
    permission_classes=(IsStaffPermission,)


    def post(self, request,*args,**kwargs):
        try:
            employee_id = request.data.get('employee_id')
            if not employee_id:
                raise Exception("Employee id is required.")
            if employee_id == request.user.id:
                raise Exception("You can't interchange shift with yourself.")
            filter_data = {"staff__employee__id": employee_id,"Day_of_week": findDayForToday(),"week_id":findOutCurrentWeekId()}
            shift_obj = self.findShiftForEmployeeId(filter_data)
            filter_data.update({"staff__employee__id": request.user.id})
            personal_shift_obj = self.findShiftForEmployeeId(filter_data)
            
            message = self.shiftInterchange(personal_shift_obj,shift_obj)
            return Response({"message": message},status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)
        
    def findShiftForEmployeeId(self,filter_data):
        shift_obj = Shift.objects.filter(**filter_data)
        if not shift_obj.exists():
            raise Exception("No shift assigned for today this staff.")
        return shift_obj.first()
    
    def shiftInterchange(self,personal_shift_obj,shift_obj):
        start_time= personal_shift_obj.start_time
        end_time = personal_shift_obj.end_time

        personal_shift_obj.start_time = shift_obj.start_time
        personal_shift_obj.end_time = shift_obj.end_time
        personal_shift_obj.save()
        shift_obj.start_time = start_time
        shift_obj.end_time = end_time
        shift_obj.save()

        return "Successfully interchange the shift timming operation"
        