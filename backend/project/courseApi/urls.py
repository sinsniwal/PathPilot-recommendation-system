from django.urls import path
from . import views

urlpatterns = [
    path("hello", views.CourseAPI.as_view(), name="course")
]
