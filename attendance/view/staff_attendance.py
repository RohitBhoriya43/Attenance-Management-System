from .imports import *

class AttendanceMarkOut(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsStaffPermission,)

    def get(self,request,*args,**kwargs):
        try:
            attendance_obj = Attendance.objects.filter(staff__employee__id=request.user.id)
            serial = AttendanceSerializer(attendance_obj,many=True)
            return Response(serial.data,status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)

    def post(self,request,*args,**kwargs):
        try:
            io_file = request.data.get("file")
            employee_id = request.user.id
            day_of_week = findDayForToday()
            read_io_file = self.check_file_data(io_file,employee_id)
            # print("read_io_file",read_io_file,type(read_io_file))
            shift_obj = Shift.objects.filter(staff__employee__id=employee_id,day_of_week=day_of_week,week_id=findOutCurrentWeekId()).first()
            if not shift_obj:
                raise Exception("No shift assigned for today.")
            current_time = (timezone.now()+timezone.timedelta(hours=5)+timezone.timedelta(minutes=30)).time()
            print("current_time",current_time)
            combine_time = (timezone.datetime.combine(timezone.now(),shift_obj.start_time)+timezone.timedelta(hours=1)).time()
            print("combine_time",combine_time)

            if not (shift_obj.start_time <= current_time <= (timezone.datetime.combine(timezone.now(),shift_obj.start_time)+timezone.timedelta(hours=1)).time()):
                raise Exception("Attendance can only be marked within 1 hour of shift start time")
            
            attendance_obj = Attendance.objects.filter(staff__employee__id=employee_id,shift=shift_obj).first()         
            if attendance_obj:
                raise Exception("Already mark out attendance")

            attendance_obj = Attendance()
            attendance_obj.staff = shift_obj.staff
            attendance_obj.shift = shift_obj
            attendance_obj.image = str(read_io_file)
            attendance_obj.save()

            return Response({"message:successfully mark out attendance"},status.HTTP_200_OK)

        except Exception as e:
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)
    

    def check_file_data(self,io_file,employee_id):
        if io_file is None:
            raise Exception("Please photo provide in payload")

        if type(io_file) != str:
            read_io_file = io_file.read()
            base64_string = base64.b64encode(read_io_file).decode('utf-8')
            return base64_string
        
        return io_file.split(",")[1] if len(io_file.split(","))==2 else io_file 
    
        