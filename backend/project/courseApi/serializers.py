from rest_framework import serializers

from .models import Feedback


# For serializing the Feedbacks object so that it can be returned as JSON
class FeedbackSerializer(serializers.ModelSerializer):
    student_roll_no = serializers.SerializerMethodField()
    course_code = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            "fid",
            "course_code",
            "student_roll_no",
            "rating",
            "title",
            "description",
        ]

    def get_student_roll_no(
        self, obj
    ):  # retrieving the roll no of the student instead of the student id.
        return obj.student.roll_no

    def get_course_code(self, obj):
        return obj.course.course_code
