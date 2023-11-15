from .utils import Model
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


def getRoadmap(courses_completed: list):
    """
    getRoadmap returns the roadmap given the completed courses
    """
    our_model = Model()
    roadmap = our_model.predict(courses_completed)
    return roadmap
    

class CourseAPI(APIView):
    def get(self, request):

        token = request.headers.get('Bearer')       

        roadmap = getRoadmap([])

        return Response({
            "message": token,
            "roadmap": roadmap
        })

