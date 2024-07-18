
# Attendance Management System with Image Capture

Firstly create a python virual environment
```bash
  python -m venv venv
```
Activate the virual Environment 1 (windows)
```bash
  source venv/Scripts/activate
```
Activate the virual Environment 2 (mac/linux)
```bash
  . venv/bin/activate
```

Install the requirements.txt file
```bash
  pip install -r requirements.txt
```
Run the django project
```bash
  python manage.py runserver 3000
```

#### Super User create command
```bash
  python manage.py createsuperuser
```


## Login Manager and Staff

# token generate api
```http
  POST /api/v1/employee/login
```
```http
    Payload 
        {
            "employee_id:"employee_id", -----> optional
            "email":"email",
            "password":"password"
        }
```


## Manage task Api


# Get All staff members
```http
    GET /api/v1/employee/manager/staff/getAll
```




# Add new staff members to the roster

```http
    POST /api/v1/employee/manager/roster/staff/create
```
Payload
```http 
        {
            "employee_id":"employee_id"
        }
```

# Set working day and shifts for each staff member

```http
    POST /api/v1/employee/manager/shift/create
```
Payload
```http
     
        {
            "employee_id":"employee_id",
            "shift_data":{
                "Monday":"9-6",
                "Tuesday":"9-6",
                "Wednesday":"9-6",
                "Thursday":"9-6",
                "Friday":"10-7"
            },
            "current_week":true,
            "next_week":false
        
        }
```


# Update shift timing per staff member

```http
    POST /api/v1/employee/manager/shift/update
```
Payload
```http 
        {
            "employee_id":"employee_id",
            "shift_data":{
                "Monday":"9-6",
                "Tuesday":"9-6",
                "Wednesday":"9-6",
                "Thursday":"9-6",
                "Friday":"10-7"
            },
            "current_week":true,
            "next_week":false
        
        }
```


# View the single staff member in roster

```http
    GET /api/v1/manager/roster/staff/<employee_id>
```

# View the All staff member in roster

```http
    GET /api/v1/manager/roster/staffs/get
```

# Set 1-2 weekly off per staff member

```http
    POST /api/v1/employee/staff/<employee_id>/rest_day/<off_day>/create
```

# View attendance per staff member or all member

```http
    GET /api/v1/employee/manager/roster/staff/attenance/get
```
Query Parameter 
```http
        employee_id=employee_id
        current_day=true
        current_week=false
```



## Staff task Api

# View their Assigned Shift

```http
    GET /api/v1/employee/staff/shift/get
```
Query Parameter 
```http
    
        current_shift_weekly= true 
        next_shift_weekly = false
```


# Mark their attendance by capturing an image using the webcam,but only within 1 hour of their shift timing.

```http
    POST /api/v1/employee/staff/attendance/mark_out
```
two type of payload
```http

    formdata
```
```http      
    {
        "file":"base64string"
    }
```

# View the Attendance

```http
    GET /api/v1/employee/staff/attendance/get
```

# Interchange the Shift

```http
  POST /api/v1/employee/staff/shift/interchange
```
Payload
```http
     
        {
            "employee_id":"employee_id"
        }
```







