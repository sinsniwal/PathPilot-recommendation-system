from django.contrib.auth.models import AbstractUser
from django.db import models

from courseApi.models import Course

# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("student", "Student"),
        ("pod", "Pod"),
    )
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="other"
    )

    def get_related_object(self):
        if self.user_type == "student":
            return Student.objects.get(user=self)
        elif self.user_type == "pod":
            return POD.objects.get(user=self)
        return None

    def __str__(self):
        return self.username


# Student Model


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True
    )  # One-to-One relationship with the user model
    roll_no = models.CharField(
        max_length=20
    )  # String field for the student's roll number
    completed_courses = models.ManyToManyField(
        "courseApi.Course"
    )  # Many-to-Many relationship for completed courses
    schedule = models.IntegerField()  # Integer field for the student's schedule
    commitment = models.IntegerField()  # Integer field for the student's commitment

    def __str__(self):
        return self.name


# Pod Model


class POD(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True
    )  # One-to-One relationship with the user model
    pod_id = models.CharField(max_length=20)  # String field for the pod's id

    def __str__(self):
        return self.name
