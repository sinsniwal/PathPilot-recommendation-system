from django.db import models


# Create your models here.
class Course(models.Model):
    scid = models.AutoField(primary_key=True)  # AutoField for a unique ID
    course_code = models.CharField(max_length=20)  # String field for the course code
    course_name = models.CharField(max_length=255)  # String field for the course name
    term = models.CharField(max_length=20)  # String field for the term
    course_type = models.CharField(max_length=20)  # String field for the type
    status = models.CharField(max_length=20)  # String field for the status
    active = models.BooleanField()  # Boolean field for active status
    comment = models.TextField()  # Text field for comments
    feedback = (
        models.JSONField()
    )  # JSON field for feedback, assuming it's a string array

    def __str__(self):
        return self.course_name
