from datetime import date,timedelta,datetime


def findDayForToday():
    today = date.today()
    day_number = today.weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return days[day_number]

def findIndexForDay(day):
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return days.index(day)

def findOutCurrentWeekId():
    return f"{(datetime.now()-timedelta(days=date.today().weekday())).date()}_{(datetime.now()+timedelta(days=6-date.today().weekday())).date()}"
    
def findOutNextWeekId():
    if date.today().weekday() ==0:
        return findOutCurrentWeekId()
    else:
        return f"{(datetime.now()+timedelta(days=6-date.today().weekday()+1)).date()}_{(datetime.now()+timedelta(days=6-date.today().weekday()+7)).date()}"


def check_str_true_false(shift_weekly):
        try:
            if not shift_weekly:
                return False
            
            if (eval(shift_weekly.capitalize())):
                return True
            return False
        except:
            raise Exception("please write the true and false value")