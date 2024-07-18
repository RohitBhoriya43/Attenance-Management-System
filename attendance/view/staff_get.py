from .imports import *


class GetAllStaff(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsManagerPermission,)

    def get(self,request,*args,**kwargs):
        try:
            Staff_obj = Employee.objects.filter(role=Role.Staff,is_superuser=False)
            serial = StaffSerializer(Staff_obj,many=True)
            return Response(serial.data,status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)