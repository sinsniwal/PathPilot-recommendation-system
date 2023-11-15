from django.urls import path
from . import views

urlpatterns = [
    path("recommend/", views.CourseAPI.as_view(), name="course")
]
