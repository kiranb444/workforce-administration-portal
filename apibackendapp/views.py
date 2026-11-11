from django.shortcuts import render
from .models import employee, department, projects, User, UserDetails
from rest_framework import viewsets
from .serializers import EmployeeSerializer, DepartmentSerializer, ProjectSerializer, UserDetailsSerializers, UserSerializer, SignupSerializer, LoginSerializer
from rest_framework import filters
from rest_framework.views import APIView
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate

# Create your views here.
#EmployeeViewset---> class name
#viewsets.ModelViewSet--->DRF class that provides implementations for CRUD operations.
class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    #collection of objects from the database using ORM
    queryset=employee.objects.all()
    serializer_class=EmployeeSerializer
    #use the searchFilter functionality..
    #Searchfilter is a built-in feature provided by django
    filter_backends=[filters.SearchFilter]
    #specifies the fields in which the search should be performed
    search_fields=['employeename', 'designation']
    #http://127.0.0.1:8000/api/employees/?search=Vishnu

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset=department.objects.all()
    serializer_class=DepartmentSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset=projects.objects.all()
    serializer_class=ProjectSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset=UserDetails.objects.all()
    serializer_class=UserDetailsSerializers

#class-based API-APIView is provided by Django REST framework
class SignupAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            #If the validation success, it will create a new user
            #DRF internally calls create() inside the serializer
            user=serializer.save()
            #If token exists, returns the existing token.otherwise it creates a new one
            # token,created=Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "user_id":user.id,
                "username":user.username,
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                # "token":token.key,
                "role":user.groups.all()[0].id if user.groups.exists() else None
            },status=status.HTTP_201_CREATED)
        else:
            res={'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes=[AllowAny]

    # Runs when POST/login is called
    def post(self,request):
        #creates a serializer object and it receives the username and password
        serializer=LoginSerializer(data=request.data)
        #serializer will validate the data
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=authenticate(request,username=username,password=password)
            if user is not None:
                refresh=RefreshToken.for_user(user)
                # token=Token.objects.get(user=user)
                response={
                    "status":status.HTTP_200_OK,
                    "message":"success",
                    "username":user.username,
                    "access":str(refresh.access_token),
                    "refresh":str(refresh),
                    #"token":token.key,
                    "role":user.groups.all()[0].id if user.groups.exists() else None
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid Email or password"
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)
        response={
            "status":status.HTTP_400_BAD_REQUEST,
            "message":"bad request",
            "data":serializer.errors
            }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

