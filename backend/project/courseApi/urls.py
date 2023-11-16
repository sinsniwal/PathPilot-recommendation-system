from django.urls import path
from . import views

urlpatterns = [
    path("recommend/", views.CourseAPI.as_view(), name="course"),
    path("feedback/<str:course_code>", views.CourseFeedbackAPI.as_view(), name="cousre_feedback"),
    path("feedback/", views.StudentFeedbackAPI.as_view(), name="student_feedback"),
    path("feedback/modify/<int:fid>", views.EditFeedbackAPI.as_view(), name="edit_feedback")
]
