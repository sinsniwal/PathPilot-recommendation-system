from .utils import Model
from authApi.models import Student
from .models import Course, Feedback
from .serializers import FeedbackSerializer
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

def student_authenticator(request):
    """
    authenticator authenticates the incoming request and validates if it contains a valid token.
    It returns a student decrypting it from the token.
    """

    a = JWTAuthentication().authenticate(request) 
    user = a[0]

    try:
        student_user = Student.objects.get(user = user)
    except:
        return Response({
            "message": "You must be a student to get recommendation!",
            "status": status.HTTP_400_BAD_REQUEST
        })

    return student_user

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
        student_user = student_authenticator(request)

        completed_courses = student_user.completed_courses.all()
        completed_courses = [course.course_code for course in completed_courses]

        roadmap = getRoadmap(completed_courses)

        return Response({
            "completed_courses": completed_courses,
            "roadmap": roadmap
        })

class CourseFeedbackAPI(APIView):
    def get(self, request, course_code):
        JWTAuthentication().authenticate(request)

        try:
            course = Course.objects.get(course_code = course_code)
        except:
            return Response({
                "message": "course associated with the given course_code doesn't exist!",
                "status": status.HTTP_400_BAD_REQUEST
            })

        feedbacks = Feedback.objects.filter(course = course).all()

        return Response({
            "course_code": course_code,
            "feedbacks": FeedbackSerializer(feedbacks, many = True).data  # many=True because it would contain a list of feedbacks
        })

class StudentFeedbackAPI(APIView):
    def get(self, request):
        student_user = student_authenticator(request)
        feedbacks = Feedback.objects.filter(student = student_user).all()

        return Response({
            "roll_no": student_user.roll_no,
            "feedbacks": FeedbackSerializer(feedbacks, many = True).data
        })

    def post(self, request):
        student_user = student_authenticator(request)

        try:
            feedback = Feedback()
            feedback.student = student_user

            course = Course.objects.get(course_code = request.data.get("course_code"))
            
            feedback.course = course
            feedback.rating = request.data.get("rating")
            feedback.title = request.data.get("title")
            feedback.description = request.data.get("description")
            feedback.save()

        except:
            return Response({
                "message": "Invalid data",
                "status": status.HTTP_400_BAD_REQUEST
            })

        return Response({
            "message": "Feedback saved successfully",
            "feedback": FeedbackSerializer(feedback).data
        })
        
class EditFeedbackAPI(APIView):
    def post(self, request, fid):
        student_user = student_authenticator(request)

        try:
            feedback = Feedback.objects.get(fid = fid)
            if feedback.student != student_user:
                return Response({
                    "message": "You cannot modify feedback of some other student",
                    "status": status.HTTP_406_NOT_ACCEPTABLE
                })

            feedback.rating = request.data.get("rating")
            feedback.title = request.data.get("title")
            feedback.description = request.data.get("description")
            feedback.save()
            
        except:
            return Response({
                "message": "Invalid data",
                "status": status.HTTP_400_BAD_REQUEST
            })
    
        return Response({
            "message": "Feedback saved successfully",
            "feedback": FeedbackSerializer(feedback).data
        })

    def delete(self, request, fid):
        student_user = student_authenticator(request)
        try:
            feedback = Feedback.objects.get(fid = fid)
            if feedback.student != student_user:
                return Response({
                    "message": "You cannot delete feedback of some other student",
                    "status": status.HTTP_406_NOT_ACCEPTABLE
                })

            feedback.delete()

        except:
            return Response({
                "message": "Invalid data",
                "status": status.HTTP_400_BAD_REQUEST
            })

        return Response({
            "message": "Feedback deleted successfully",
        })