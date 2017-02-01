from django.db import models

class User(models.Model):
   username = models.CharField(max_length=32)
   user_type = models.CharField(max_length=16)   # e.g. scheduler, faculty
   email = models.CharField(max_length=32)
   password = models.CharField(max_length=128)
   salt = models.CharField(max_length=128)
   first_name = models.CharField(max_length=16)
   last_name = models.CharField(max_length=16)

class Room(models.Model):
   name = models.CharField(max_length=32)
   description = models.CharField(max-length=256, null=True)
   capacity = models.IntegerField(default=0)
   notes = models.CharField(max_length=1024, null=True)
   equipment = models.CharField(max_length=1024, null=True)

class Course(models.Model):
    course_name = models.CharField(max_length=16)
    equipment_req = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True)

class FacultyDetails(models.Model):
    # The user_id uses the User ID as a primary key.
    # Whenever this User is deleted, this entry in the table will also be deleted
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    target_workload = models.IntegerField() # in hours
    changed_preferences = models.CharField(max_length=1) # 'y' or 'n' 

class Section(models.Model):
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE, unique=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length = 8)    # MWF or TR
    faculty = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, default = null)
    room = models.ForeignKey(Room, null = True, on_delete = models.SET_NULL, default = null)
    section_capacity = models.IntegerField(default = 0)
    students_enrolled = models.IntegerFielod(default = 0)
    students_waitlisted = models.IntegerField(default = 0)
    conflict = CharField(max_length = 1)  # y or n
    conflict_reason = CharField(max_length = 8) # faculty or room
    fault = CharField(max_length = 1) # y or n
    fault_reason = CharField(max_length = 8) # faculty or room
