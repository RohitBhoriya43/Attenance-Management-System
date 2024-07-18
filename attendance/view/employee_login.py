from .imports import *

class EmployeeLogin(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self,request,*args,**kwargs):
        try:
            employee_obj,token = self.check_all_field_and_employee_data(request.data)
            return Response(token,status.HTTP_200_OK)    
        except Exception as e:
            return Response({"errors":str(e)},status.HTTP_400_BAD_REQUEST)
        
    
    def check_all_field_and_employee_data(self,data):
        employee_id = data.get("employee_id")
        email = data.get("email")
        password = data.get("password")

        if employee_id or not email:
            print("employee_id",employee_id,"email",email)
            raise Exception("please provide the email ya employee id")
        
        if not password:
            raise Exception("please provide the password")
        
        if employee_id is None and email is not None:
            user_obj = self.filter_data({"email":email})
        elif employee_id is not None and email is None:
            user_obj = self.filter_data({"employee_id":employee_id})
        
        if not user_obj.check_password(password):
            raise Exception("Invalid Credentials")
        
        token = get_tokens_for_user(user_obj)
        return user_obj,token

    def filter_data(self,data):
        user_obj = Employee.objects.filter(**data)
        if user_obj.exists():
            user_obj = user_obj.first()
        else:
            raise Exception("User does not exists")

        return user_obj
        