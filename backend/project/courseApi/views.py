from .utils import Model
from authApi.models import Student
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

#TODO: create tests for getRoadmap()
def getRoadmap(courses_completed: list):
    """
    getRoadmap returns the roadmap given the completed courses
    """
    our_model = Model()
    roadmap = our_model.predict(courses_completed)
    return roadmap
    

class CourseAPI(APIView):
    def get(self, request):
        a = JWTAuthentication().authenticate(request) 
        user = a[0]

        try:
            student_user = Student.objects.get(user = user)
        except:
            return Response({
                "message": "You must be a student to get recommendation!",
                "status": status.HTTP_400_BAD_REQUEST
            })

        completed_courses = student_user.completed_courses.all()
        completed_courses = [course.course_code for course in completed_courses]

        roadmap = getRoadmap(completed_courses)

        return Response({
            "completed_courses": completed_courses,
            "roadmap": roadmap
        })

