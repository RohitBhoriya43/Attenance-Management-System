from .imports import *

class StaffWeeklyOff(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsManagerPermission,)

    def post(self,request,*args,**kwargs):
        try:
            employee_id = kwargs.get('employee_id')
            rest_day = self.check_rest_day(kwargs.get('rest_day'))
            staff_roaster = self.find_out_staff_roster_obj(employee_id)
            current_week_rest_data,current_week,rest_data = self.get_current_week_rest_data(staff_roaster.weekly_off,rest_day)
            if rest_day.capitalize() in current_week_rest_data:
                raise Exception("Rest day already added for this week")
            current_week_rest_data.append(rest_day.capitalize())
            self.add_rest_day_obj_in_model(staff_roaster,rest_data,{current_week:current_week_rest_data})

            return Response({"message":"rest day successfully added"},status.HTTP_201_CREATED)           

        except Exception as e:
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)
        
    def check_rest_day(self,rest_day):
        try:
            return DayOfWeek[rest_day.capitalize()]
        except Exception as e:
            raise Exception("Invalid rest_day, please write the day of the week")
    
    def find_out_staff_roster_obj(self,employee_id):
        staff_roster = StaffRoster.objects.filter(employee__id=employee_id)
        if not staff_roster.exists():
            raise Exception("There is no staff member this employee id")
        return staff_roster.first()
    
    def get_current_week_rest_data(self,rest_obj,rest_day): 
        if findIndexForDay(rest_day.capitalize()) <= findIndexForDay(findDayForToday()):
            raise Exception("current day can not be add the rest day")

        current_week = findOutCurrentWeekId()
        # print(current_week)
        rest_data = json.loads(rest_obj) if rest_obj is not None else {}
        if current_week in rest_data:
            # print(rest_data[current_week])
            if len(rest_data[current_week]) <2:
                # print(rest_data[current_week])
                return rest_data[current_week],current_week,rest_data
            else:
                raise Exception("Rest data for current week is already full")
        else:
            return {current_week:[]},current_week,rest_data
    
    def add_rest_day_obj_in_model(self,staff_roaster,rest_data,current_week_rest_data):
        rest_data.update(current_week_rest_data)
        staff_roaster.weekly_off = str(json.dumps(rest_data))
        staff_roaster.save()
        return True
        
        
    
    
        