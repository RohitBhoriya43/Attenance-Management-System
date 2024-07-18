from .imports import *

class ShiftStaffView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsStaffPermission,)

    def get(self,request,*args,**kwargs):
        try:
            current_shift_weekly = self.check_weekly_shift_query(request.query_params.get("current_shift_weekly"))
            next_shift_weekly = self.check_weekly_shift_query(request.query_params.get("next_shift_weekly"))
            employee_id = request.user.id
            shiftSerializer = ShiftSerializer(self.check_current_shift_weekly_next_shift_weekly({"staff__employee__id":employee_id},current_shift_weekly,next_shift_weekly),many=True)
            return Response(shiftSerializer.data,status.HTTP_200_OK)
        except Exception as e:
            
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)
    
    def check_weekly_shift_query(self,shift_weekly):
        try:
            if not shift_weekly:
                return False
            
            if (eval(shift_weekly.capitalize())):
                return True
            return False
        except:
            raise Exception("Invalid shift_weekly,please write the true and false value")
        
    def check_current_shift_weekly_next_shift_weekly(self,filter_data,current_weekly,next_weekly):
        if current_weekly and not next_weekly:
            filter_data.update({"week_id":findOutCurrentWeekId()})
        elif next_weekly and not current_weekly:
            filter_data.update({"week_id":findOutNextWeekId()})
        else:
            filter_data.update({"day_of_week":findDayForToday(),"week_id": findOutCurrentWeekId()})
        return self.find_out_shift_obj(filter_data)
    

    def find_out_shift_obj(self,filter_data):
        return Shift.objects.filter(**filter_data)

