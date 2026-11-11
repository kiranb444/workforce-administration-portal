from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class department(models.Model):
    departmentID=models.AutoField(primary_key=True)
    departmentname=models.CharField(max_length=100)

    def __str__(self):
        return self.departmentname

class employee(models.Model):
    employeeid=models.AutoField(primary_key=True)
    employeename=models.CharField(max_length=100)
    designation=models.CharField(max_length=100)
    dateofjoining=models.DateField()
    departmentid=models.ForeignKey(department,on_delete=models.CASCADE)
    contact=models.CharField(max_length=15)
    isactive=models.BooleanField(default=True)

    def __str__(self):
            return self.employeename

class projects(models.Model):
     #for a many to many relationship model, we cannot explicity define
     #an id field.Django will be referring to the default id field.
     name=models.CharField(max_length=100,unique=True)
     #define many to many field
     #related name of this relation will be later reffered in the serializer
     employees=models.ManyToManyField(employee,related_name='projects')

     def __str__(self):
          return self.name


class UserDetails(models.Model):
     user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_details')
     phoneno=models.CharField(max_length=15)
     email=models.EmailField()

     def __str__(self):
          return self.user.username