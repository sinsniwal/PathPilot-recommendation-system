from django.db.models import Avg
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from authApi.models import Student

from .models import Course, Feedback
from .serializers import FeedbackSerializer
from .utils import Model
from django.shortcuts import render

# Create your views here.


def student_authenticator(request):
    """
    student_authenticator authenticates the incoming request and validates if it contains a valid token.
    It returns a student decrypting it from the token.
    """

    a = JWTAuthentication().authenticate(request)
    user = a[0]

    try:
        student_user = Student.objects.get(user=user)
    except:
        return None, Response(
            {
                "message": "You must be a student to get recommendation!",
            }, status=status.HTTP_400_BAD_REQUEST
        )

    return student_user, None


def course_authenticator(request, course_code):
    """
    course_authenticator authenticates the incoming request and validates if it contains a valid token.
    It returns a course associated with the given course_code.
    """

    JWTAuthentication().authenticate(request)

    try:
        course = Course.objects.get(course_code=course_code)
    except:
        return None, Response(
            {
                "message": "course associated with the given course_code doesn't exist!",
            }, status=status.HTTP_400_BAD_REQUEST
        )

    return course, None


# TODO: create tests for getRoadmap()
def getRoadmap(courses_completed: list):
    """
    getRoadmap returns the roadmap given the completed courses
    """
    our_model = Model()
    roadmap = our_model.predict(courses_completed)
    return roadmap


class CourseAPI(APIView):
    def get(self, request):
        student_user, err = student_authenticator(request)
        if err != None:
            return err

        completed_courses = student_user.completed_courses.all()
        completed_courses = [course.course_code for course in completed_courses]
        completed_courses_names = [ (course.course_code, course.course_name) for course in student_user.completed_courses.all()]
        roadmap = getRoadmap(completed_courses)

        return Response({"completed_courses": completed_courses, "roadmap": roadmap, "completed_courses_names": completed_courses_names})


class CourseFeedbackAPI(APIView):
    def get(self, request, course_code):
        course, err = course_authenticator(request, course_code)
        if err != None:
            return err

        feedbacks = Feedback.objects.filter(course=course).all()

        return Response(
            {
                "course_code": course_code,
                "course_name": course.course_name,
                "feedbacks": FeedbackSerializer(
                    feedbacks, many=True
                ).data,  # many=True because it would contain a list of feedbacks
            }
        )


class StudentFeedbackAPI(APIView):
    def get(self, request):
        student_user, err = student_authenticator(request)
        if err != None:
            return err

        feedbacks = Feedback.objects.filter(student=student_user).all()
        return Response(
            {
                "roll_no": student_user.roll_no,
                "feedbacks": FeedbackSerializer(feedbacks, many=True).data,
            }
        )

    def post(self, request):
        student_user, err = student_authenticator(request)
        if err != None:
            return err

        try:
            feedback = Feedback()
            feedback.student = student_user
            print(request.data)
            try:
                course = Course.objects.get(course_code=request.data.get("course_code"))
            except:
                course= Course.objects.get(course_name=request.data.get("courseode"))
            feedback.course = course
            feedback.rating = request.data.get("rating")
            feedback.title = request.data.get("title")
            feedback.description = request.data.get("description")
            feedback.save()

        except:
            return Response(
                {"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Feedback saved successfully",
                "feedback": FeedbackSerializer(feedback).data,
            }
        )


class EditFeedbackAPI(APIView):
    def post(self, request, fid):
        student_user, err = student_authenticator(request)
        if err != None:
            return err

        try:
            feedback = Feedback.objects.filter(fid=int(fid)).first()
            print(feedback.student,student_user)
            if feedback.student != student_user:
                return Response(
                    {
                        "message": "You cannot modify feedback of some other student",
                    }, status=status.HTTP_406_NOT_ACCEPTABLE
                )
            print(request.data.get("rating"),request.data.get("title"),request.data.get("description"))
            feedback.rating = int(request.data.get("rating"))
            feedback.title = request.data.get("title")
            feedback.description = request.data.get("description")
            feedback.save()

        except Exception as e:
            print(e)
            return Response(
                {"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST}
            )

        return Response(
            {
                "message": "Feedback saved successfully",
                "feedback": FeedbackSerializer(feedback).data,
            }
        )

    def delete(self, request, fid):
        student_user, err = student_authenticator(request)
        if err != None:
            return err

        try:
            feedback = Feedback.objects.get(fid=fid)
            if feedback.student != student_user:
                return Response(
                    {
                        "message": "You cannot delete feedback of some other student",
                    }, status=status.HTTP_406_NOT_ACCEPTABLE
                )

            feedback.delete()

        except:
            return Response(
                {"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Feedback deleted successfully",
            }
        )


class CourseStatsAPI(APIView):
    def get(self, request, course_code):
        course, err = course_authenticator(request, course_code)
        if err != None:
            return err

        average_rating = Feedback.objects.filter(course=course).aggregate(
            Avg("rating")
        )["rating__avg"]
        n_students = Student.objects.filter(completed_courses=course).count()

        return Response(
            {
                "course_code": course_code,
                "course_name": course.course_name,
                "average_rating": average_rating,
                "n_students": n_students,
            }
        )


class LevelStatsAPI(APIView):
    def get(self, request, level):
        JWTAuthentication().authenticate(request)

        level_courses = Course.objects.filter(level=level).all()
        average_rating = Feedback.objects.filter(course__in=level_courses).aggregate(
            Avg("rating")
        )["rating__avg"]
        n_students = (
            Student.objects.filter(completed_courses__in=level_courses)
            .distinct()
            .count()
        )

        return Response(
            {
                "level": level,
                "average_rating": average_rating,
                "n_students_completed_some_course_in_level": n_students,
            }
        )
