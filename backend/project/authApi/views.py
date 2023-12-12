from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import POD, CustomUser, Student
from django.shortcuts import render


# Create your views here.
@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello, world!", "status": 200})


@api_view(["GET"])
def isLoggedin(request):
    a = JWTAuthentication().authenticate(request)
    if a:
        return Response({"message": "User is logged in."})
    else:
        return Response({"message": "User is not logged in."})


class LoginAPI(APIView):
    def post(self, request):
        if request.method == "POST":
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response(
                    {
                        "message": "Username and password are required.",
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                )

            user = CustomUser.objects.filter(username=username).first()
            print(user)
            if user:
                authenticated_user = authenticate(username=username, password=password)
                if authenticated_user:
                    refresh = RefreshToken.for_user(user)
                    print("Validated")
                    return Response(
                        {
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                            "status": 200,
                            "usertype": user.user_type,
                        }
                    )
                    return render(request, "blog.html")
                else:
                    return Response({"message": "Invalid Credentials", "status": 400})
            else:
                return Response({"message": "User does not exist", "status": 400})


class RegisterAPI(APIView):
    def post(self, request):
        try:
            if CustomUser.objects.filter(
                username=request.data.get("username")
            ).exists():
                return Response({"message": "Username already exists", "status": 400})
            if request.data.get("user_type") == "student":
                try:
                    # first create customUser
                    # create student
                    user = CustomUser()
                    user.username = request.data.get("username")
                    user.first_name = request.data.get("first_name")
                    user.last_name = request.data.get("last_name")
                    user.email = request.data.get("email")
                    user.set_password(request.data.get("password"))
                    user.user_type = request.data.get("user_type")
                    user.save()
                    student = Student()
                    student.user = user
                    student.roll_no = request.data.get("roll_no")
                    student.save()
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                            "status": 200,
                            "usertype": user.user_type,
                        }
                    )
                except:
                    return Response({"message": "Invalid Data", "status": 400})
            elif request.data.get("user_type") == "pod":
                try:
                    # first create customUser
                    # create student
                    user = CustomUser()
                    user.username = request.data.get("username")
                    user.first_name = request.data.get("first_name")
                    user.last_name = request.data.get("last_name")
                    user.email = request.data.get("email")
                    user.set_password(request.data.get("password"))
                    user.user_type = request.data.get("user_type")
                    user.save()

                    pod = POD()
                    pod.user = user
                    pod.pod_id = request.data.get("roll_no")
                    pod.save()

                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                            "status": 200,
                            "usertype": user.user_type,
                        }
                    )
                except:
                    return Response({"message": "Invalid Data", "status": 400})
            else:
                return Response({"message": "Invalid Data", "status": 400})
        except:
            return Response({"message": "Invalid Data", "status": 400})

