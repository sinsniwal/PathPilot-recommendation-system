from rest_framework.test import APITestCase
from authApi.models import CustomUser, Student
from .models import Course, Feedback

# Create your tests here.
class CourseTestCase(APITestCase):

    def setUp(self):

        self.student = CustomUser.objects.create_user(
            username = "student",
            user_type="student", 
            password = "mypassword",
            first_name="as",
            last_name="last",
            email="23425",
        )

        studentProfile = Student.objects.create(user=self.student, roll_no="43564")

        self.notStudent = CustomUser.objects.create_user(
            username="notstudent", password="mypassword2"
        )

        studentResponse = self.client.post("/api-auth/login/", {
            "username": "student",
            "password": "mypassword"
        })

        self.studentToken = studentResponse.data["access"]

        notstudentResponse = self.client.post("/api-auth/login/", {
            "username": "notstudent",
            "password": "mypassword2"
        })

        self.notstudentToken = notstudentResponse.data["access"]

    def test_recommend(self):

        response = self.client.get(
            "/course/recommend/", HTTP_AUTHORIZATION="Bearer " + self.studentToken
        )

        self.assertEqual(type(response.data['completed_courses']), list)
        self.assertEqual(type(response.data['roadmap']), list)

    def test_notstudent(self):

        response = self.client.get(
            "/course/recommend/", HTTP_AUTHORIZATION="Bearer " + self.notstudentToken
        )

        self.assertEqual(response.status_code, 400)

class CourseFeedbackTestCase(APITestCase):

    def setUp(self):

        self.student = CustomUser.objects.create_user(
            username = "student",
            user_type="student", 
            password = "mypassword",
            first_name="as",
            last_name="last",
            email="23425",
        )

        studentProfile = Student.objects.create(user=self.student, roll_no="43564")
        studentResponse = self.client.post("/api-auth/login/", {
            "username": "student",
            "password": "mypassword"
        })

        self.studentToken = studentResponse.data["access"]

        course1 = Course.objects.create(
            course_code="BSMA1001", 
            course_name="Mathematics-1", 
            description="Mathematics part 1 for data science",
            level="foundation"
        )

        course2 = Course.objects.create(
            course_code="BSMA1002", 
            course_name="Statistics-1", 
            description="Statistics part 1 for data science",
            level="foundation"
        )

        course3 = Course.objects.create(
            course_code="BSMA1004", 
            course_name="Statistics-2", 
            description="Statistics part 2 for data science",
            level="foundation"
        )

        studentProfile.completed_courses.add(course1, course2)

        feedback = Feedback.objects.create(
            student = studentProfile,
            course = course1,
            rating = 4,
            title = "Good",
            description = "Course is good",
        )

    def test_getStudentFeedbacks(self):

        response = self.client.get(
            "/course/feedback/", HTTP_AUTHORIZATION="Bearer " + self.studentToken
        )

        self.assertEqual(type(response.data['roll_no']), str)
        self.assertEqual(response.status_code, 200)

    def test_postStudentFeedbackMoreThanOnce(self):

        data = {
            "course_code": "BSMA1001",
            "rating": "3",
            "title": "Average",
            "description": "Ok! But can be improved"
        }

        response = self.client.post("/course/feedback/", HTTP_AUTHORIZATION="Bearer " + self.studentToken, data=data)

        self.assertEqual(response.status_code, 400)

    def test_postStudentFeedbackFirstTime(self):

        data = {
            "course_code": "BSMA1002",
            "rating": "3",
            "title": "Average",
            "description": "Ok! But can be improved"
        }

        response = self.client.post("/course/feedback/", HTTP_AUTHORIZATION="Bearer " + self.studentToken, data=data)

        self.assertEqual(response.status_code, 200)

    def test_editFeedback(self):

        data = {
            "course_code": "BSMA1002",
            "rating": "4",
            "title": "Edited",
            "description": "Ok! But can be improved"
        }

        response = self.client.post("/course/feedback/modify/1", HTTP_AUTHORIZATION="Bearer " + self.studentToken, data=data)
        self.assertEqual(response.status_code, 200)

    def test_deleteFeedback(self):

        response = self.client.delete("/course/feedback/modify/1", HTTP_AUTHORIZATION="Bearer " + self.studentToken)
        self.assertEqual(response.status_code, 200)

    def test_getCourseStat(self):

        response = self.client.get("/course/stats/course/BSMA1001", HTTP_AUTHORIZATION="Bearer " + self.studentToken)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data['average_rating']), float)
        self.assertEqual(type(response.data['n_students']), int)

    def test_getLevelStat(self):
        response = self.client.get("/course/stats/level/foundation", HTTP_AUTHORIZATION="Bearer " + self.studentToken)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data['average_rating']), float)
        self.assertEqual(type(response.data["n_students_completed_some_course_in_level"]), int)
 