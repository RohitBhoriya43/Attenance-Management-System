from .imports import *



class RosterView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsManagerPermission,)

    def get(self,request,*args,**kwargs):
        try:
            employee_id = kwargs.get('employee_id')
            if employee_id:
                print(employee_id)
                roster_data = StaffRoster.objects.filter(employee__id=employee_id)
                if not roster_data.exists():
                    raise Exception("No roster data found for this employee.")
                employee_obj = roster_data.values(employeeId=F("employee__id"),full_name=F("employee__full_name"),email=F("employee__email"),username=F("employee__username"),role=F("employee__role"))[0]
                shift_obj = Shift.objects.filter(staff =roster_data.first(),week_id=findOutCurrentWeekId())
                if not shift_obj.exists():
                    shifts = {"shifts":[]}
                shifts = {"shifts":shift_obj.values("week_id","day_of_week","start_time","end_time")}
                data = self.set_roster_data({"employee": employee_obj},shifts,roster_data.first().id,roster_data.first().weekly_off)
            else:
                print(employee_id,"else")
                roster_data = StaffRoster.objects.all()
                data = self.set_all_roster_data(roster_data)
            return Response(data,status.HTTP_200_OK)
                
        except Exception as e:
            
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)

    def post(self,request,*args,**kwargs):
        try:
            employee_id = request.data.get("employee_id")
            staff_roster = self.create_staff_roster(employee_id)
            # shift_data = request.data.get("shift_data")
            # # weekly_off = request.data.get("weekly_off")
            # self.create_shift_models_per_user(shift_data,staff_roster)
            return Response({"message":"staff roster is created successfully"},status.HTTP_200_OK)
        except Exception as e:

            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)

    def put (self,request,*args,**kwargs):
        try:
            pass

        except Exception as e:

            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)
    
    def create_staff_roster(self,employee_id):
        employee_obj = Employee.objects.filter(id=employee_id)
        if employee_obj.exists():
            employee_obj = employee_obj.first()
            if employee_obj.role!='staff':
                raise Exception("Only users with the 'staff' role can be added as staff members.") 
            staffRoster = StaffRoster.objects.filter(employee=employee_obj)
            if staffRoster.exists():
                raise Exception("Already create this staff roster")
            staffRoster = StaffRoster()
            staffRoster.employee = employee_obj
            staffRoster.save()
            return staffRoster
        else:
            raise Exception("Employee id does not exists")
        

    def create_shift_models_per_user(self,shift_data,staff_roster):
        thread = threading.Thread(target=self.create_shift_data,args=(shift_data,staff_roster))

    def create_shift_data(self,shift_data,staff_roster):
        for key,value in shift_data.items():
            shift_data = Shift.objects.filter(day_of_week = key.capitalize(),staff=staff_roster)
            if not shift_data.exist():
                pass
            else:
                start_time,end_time = self.convert_time_obj(value)
                shift = Shift(staff=staff_roster,day_of_week=key.capitalize(),start_time=start_time,end_time=end_time)
                shift.save() 

    def convert_time_obj(self,value):
        time_data = value.split("-")
        start_time,end_time = time_data[0],time_data[1]
        start_format,end_format = self.convert_format_time(start_time),self.convert_format_time(end_time)
        start = datetime.strptime(start_time,start_format).time()
        end = datetime.strptime(end_time,start_format).time()

        return start,end

    def convert_format_time(time):
        try:
            time = time.split(":")[1]
            return "%H:%M"
        except:

            return "%H"
        
    
    def set_roster_data(self,employee_obj,shifts,roster_id,weekly_off=None):
        data = {"weekly_off":weekly_off,"roster_id":roster_id}
        # print(data)
        data.update(employee_obj)
        # print("data.update(employee_obj)",data)
        data.update(shifts)
        return data
    

    def set_all_roster_data(self,roster_data):

        data = []
        week_id = findOutCurrentWeekId()
        for roster in roster_data:
            employee_obj = Employee.objects.filter(id=roster.employee.id)
            if employee_obj.exists():
                employee_obj = list(employee_obj.values("id","full_name","email","username","role"))[0]
                # staffSerializer = StaffSerializer(employee_obj)
                shifts = Shift.objects.filter(staff=roster,week_id=week_id)
                shifts = shifts.values("week_id","day_of_week","start_time","end_time")
                # print(shifts)
                data.append(self.set_roster_data({"employee": employee_obj},{"shifts":shifts},roster.id,roster.weekly_off))
        return data
        