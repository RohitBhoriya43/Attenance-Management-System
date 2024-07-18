from .imports import *



class ShiftView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsManagerPermission,)

    def get(self,request,*args,**kwargs):
        try:
            pass

        except Exception as e:
            
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)

    def post(self,request,*args,**kwargs):
        try:
            self.shift_create_and_update(request)
            return Response({"message":f"{request.user.id} shift is created successfully"},status.HTTP_200_OK)
        except Exception as e:

            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)

    def put (self,request,*args,**kwargs):
        try:
            self.shift_create_and_update(request,request.method)
            return Response({"message":f"{request.user.id} shift is update successfully"},status.HTTP_200_OK)

        except Exception as e:

            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)
        
    def shift_create_and_update(self,request,method=None):
        employee_id = request.data.get("employee_id")
        staff_roster = self.find_out_roster(employee_id)
        shift_data = request.data.get("shift_data")
        current_week = request.data.get("current_week")
        next_week= request.data.get("next_week")
        # weekly_off = request.data.get("weekly_off")
        self.create_shift_models_per_user(shift_data,staff_roster,current_week,next_week,method)
        return True
    
    def find_out_roster(self,employee_id):
        
        staffRoster = StaffRoster.objects.filter(employee__id=employee_id)
        if not staffRoster.exists():
            raise Exception("There is no staff member this employee id")
        
        return staffRoster.first()
        
        

    def create_shift_models_per_user(self,shift_data,staff_roster,current_week,next_week,method=None):
        week_id= findOutCurrentWeekId()
        if next_week and not current_week:
            week_id = findOutNextWeekId()
        else:
            next_week = False
        print("week_id in before threading call data",week_id)
        thread = threading.Thread(target=self.create_shift_data,args=(shift_data,staff_roster,week_id,next_week,method))
        thread.start()

    def create_shift_data(self,shift_data,staff_roster,week_id,next_week,method=None):
        # print("nextweek",next_week)
        for key,value in shift_data.items():
            try:
                # print("findIndexForDay(key.capitalize())",findIndexForDay(key.capitalize()),"findIndexForDay(findDayForToday()))",findIndexForDay(findDayForToday()))
                findIndexForKey=findIndexForDay(key.capitalize())
                findIndexForCurrentDay =findIndexForDay(findDayForToday())
                if ( findIndexForKey>=findIndexForCurrentDay ) or next_week:
                    if DayOfWeek[key.capitalize()]:
                        shift_data = Shift.objects.filter(day_of_week = key.capitalize(),staff=staff_roster,week_id=week_id)
                        if not shift_data.exists() and not method:
                            start_time,end_time = self.convert_time_obj(value)
                            shift = Shift(staff=staff_roster,day_of_week=key.capitalize(),start_time=start_time,end_time=end_time,week_id=week_id)
                            shift.save()
                            print("shift data is store",shift)
                        else:
                            if (method == "PUT" and shift_data.exists()) and ( (findIndexForKey>findIndexForCurrentDay) or next_week  ):
                                shift_data = shift_data.first()
                                start_time,end_time = self.convert_time_obj(value)
                                shift_data.start_time = start_time
                                shift_data.end_time = end_time
                                shift_data.save()
            except Exception as e:
                print(f"Error creating shift for {key} - {e}")
                continue

    def convert_time_obj(self,value):
        time_data = value.split("-")
        start_time,end_time = time_data[0],time_data[1]
        start_format,end_format = self.convert_format_time(start_time),self.convert_format_time(end_time)
        start = datetime.strptime(start_time,start_format).time()
        end = datetime.strptime(end_time,start_format).time()
        print("coverted time",start,end)
        return start,end

    def convert_format_time(self,time):
        try:
            time = time.split(":")[1]
            return "%H:%M"
        except:

            return "%H"
        