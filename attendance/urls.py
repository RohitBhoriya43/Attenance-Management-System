from django.urls import path
from attendance.view.employee_login import EmployeeLogin
from attendance.view.shift_interchange import ShiftInterchange
from attendance.view.shift_manager import ShiftView
from attendance.view.shift_staff import ShiftStaffView
from attendance.view.roster import RosterView
from attendance.view.staff_attendance import AttendanceMarkOut
from attendance.view.staff_get import GetAllStaff
from attendance.view.staff_weekly_off import StaffWeeklyOff
from attendance.view.view_attendance import ViewAttendance

urlpatterns = [
    path('login',EmployeeLogin.as_view(),name="login employee"),
    path('manager/shift/create',ShiftView.as_view(),name="create shift per employee"),
    path('manager/shift/update',ShiftView.as_view(),name="update shift per employee"),
    path('manager/staff/getAll',GetAllStaff.as_view(),name="get all staff"),
    path('manager/roster/staff/create',RosterView.as_view(),name="create new staff in roster"),
    path('manager/roster/staff/attenance/get',ViewAttendance.as_view(),name="get attendance"),
    path('manager/roster/staff/<employee_id>',RosterView.as_view(),name="get roster from employee_id"),
    path('manager/roster/staffs/get',RosterView.as_view(),name="get All roster"),
    path('staff/shift/get',ShiftStaffView.as_view(),name="get shift data per emoployee"),
    path('staff/attendance/mark_out',AttendanceMarkOut.as_view(),name="mark out attendance"),
    path('staff/attendance/get',AttendanceMarkOut.as_view(),name="get attendance"),
    path('staff/shift/interchange',ShiftInterchange.as_view(),name="shift interchange"),
    path('staff/<employee_id>/rest_day/<rest_day>/create',StaffWeeklyOff.as_view(),name="rest day created"),
]
