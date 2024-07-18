from  rest_framework.permissions import BasePermission


class IsManagerPermission(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == "manager"
    
class IsStaffPermission(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == "staff"