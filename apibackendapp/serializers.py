from rest_framework import serializers
from .models import department, employee, projects, User, UserDetails
from datetime import date
import re
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


#validation 1: dateOfJoining current date
#validation 2: employeeName should be characters, no special character
#validation of dateOfjoining
def date_of_joining_restriction(dateofjoining):
    today=date.today()
    if dateofjoining!=today:
        raise serializers.ValidationError("The date of joining must be today")
    return dateofjoining

#validation for employeeName
def name_validation(employeename):
    if len(employeename)<3 or not re.match("^[A-Za-z]+$",employeename):
        raise serializers.ValidationError("Name must be atleast 3 letters and contain" \
                                          "only alphabetic characters.")
    return employeename
    
#validation for designation
def designation_validation(designation):
    if len(designation)<2 or not re.match("^[A-Za-z ]+$",designation):
        raise serializers.ValidationError("Designation must be atleast 2 letters and contain "\
                                          "only alphabetic characters and spaces.")
    return designation

#validation for contact
def contact_validation(contactnumber):
    if not re.match("^[0-9]{10}$", contactnumber):
        raise serializers.ValidationError("Contact number must be a 10 digit number")
    return contactnumber

#Department serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=department
        fields='__all__'

#Employee serializer
class EmployeeSerializer(serializers.ModelSerializer):
    Department=DepartmentSerializer(source='departmentid', read_only=True)

    dateofjoining=serializers.DateField(validators=[date_of_joining_restriction])
    employeename=serializers.CharField(max_length=200, validators=[name_validation])
    designation=serializers.CharField(max_length=100, validators=[designation_validation])
    contact=serializers.CharField(max_length=10, validators=[contact_validation])
    #show project details
    project_details=serializers.StringRelatedField(source='projects', many=True, read_only=True)

    class Meta:
        model=employee
        fields=('employeeid', 'employeename', 'designation', 'dateofjoining', 'contact',
                'isactive', 'departmentid', 'Department', 'project_details')

#Project serializer
class ProjectSerializer(serializers.ModelSerializer):
    #employees--->get the data for employee_details from the employees field of the
    #project model
    employee_details=EmployeeSerializer(source='employees', required=False,many=True,read_only=True)

    class Meta:
        model=projects
        fields=('id', 'name', 'employees', 'employee_details')

class UserDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model=UserDetails
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('id','username')

#Receives the registration data, validates it and hashes the password, creates the user
#amd assigns the user to a group and finally returns the created user
class SignupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        group_name=validated_data.pop('group_name', None)

        #Hash the password
        validated_data['password']=make_password(validated_data["password"])

        #create the user
        user = super(SignupSerializer,self).create(validated_data)

        if group_name:
            group,created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user

    class Meta:
        model=User
        fields=['username', 'password', 'group_name']

class LoginSerializer(serializers.ModelSerializer):
    #Field to get username from user
    username = serializers.CharField()
    #field to get password from user
    password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields = ['username', 'password']