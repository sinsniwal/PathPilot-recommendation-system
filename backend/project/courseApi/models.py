from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Course model


class Course(models.Model):
    course_code = models.CharField(
        max_length=20, primary_key=True
    )  # String field for the course code
    course_name = models.CharField(max_length=255)  # String field for the course name
    description = models.TextField()  # Text field for description
    level = models.TextChoices("level", "foundation diploma bsc bs")
    # Text field for level

    level = models.CharField(max_length=20, choices=level.choices)

    def __str__(self):
        return self.course_name


# Feedback model


class Feedback(models.Model):
    fid = models.AutoField(primary_key=True)  # Feedback Id
    student = models.ForeignKey("authApi.student", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Associated course
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating should be atleast 1"),
            MaxValueValidator(5, message="Rating should be atmost 5"),
        ]
    )  # Student's rating for the course between 1 to 5
    title = models.CharField(max_length=40)  # Title for Feeback
    description = models.TextField(max_length=150)  # Description for Feedback

    def __str__(self):
        return f"{self.course.course_name}: Rating({self.rating}), Title({self.title})"

    def clean(
        self,
    ):  # A student must have completed the course in order to register for it.
        if self.course not in self.student.completed_courses.all():
            raise ValidationError("Student hasn't completed this course!")
