from django.db import models

class Role(models.TextChoices):
    Manager = "manager"
    Staff = "staff"
    
class DayOfWeek(models.TextChoices):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"
