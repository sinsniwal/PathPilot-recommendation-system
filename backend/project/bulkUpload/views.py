from io import BytesIO

import pandas as pd
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from authApi.models import POD, CustomUser, Student  # Import your Django models
from courseApi.models import Course, Feedback  # Import your Django models
from rest_framework.decorators import api_view

@user_passes_test(lambda u: u.is_superuser)
@api_view(["GET", "POST"])
def bulkUpload(request):

    if request.method == "POST":
    
        excel_file = request.FILES["excel_file"]

        # Read the Excel file into a dictionary of DataFrames, with sheet names as keys
        excel_data = read_excel(excel_file)

        # Create bulk objects for each model
        course_message = (create_bulk_course(excel_data.get("Course")),)
        student_message = (create_bulk_student(excel_data.get("Student")),)
        pod_message = (create_bulk_pod(excel_data.get("POD")),)
        feedback_message = create_bulk_feedback(excel_data.get("Feedback"))
        # Get sheet names
        if student_message and pod_message and course_message and feedback_message:
            jobs = "All sheets uploaded successfully"
        else:
            jobs = "Some Sheets Failed To Upload: "
            # now get the sheet names which failed
            output = []
            if not student_message:
                output.append("Student")
            if not pod_message:
                output.append("POD")
            if not course_message:
                output.append("Course")
            if not feedback_message:
                output.append("Feedback")
            jobs += ",".join(output)
        sheet_names = excel_data.keys()

        sheet_data = {}
        for sheet_name in sheet_names:
            df = excel_data[sheet_name]
            sheet_data[sheet_name] = df.to_dict(orient="records")

        # Redirect or render as needed
        return render(
            request, "bulkUpload.html", {"message": jobs, "excel_data": sheet_data}
        )

    return render(request, "bulkUpload.html", {"message": "", "excel_data": ""})


def read_excel(excel_file):
    # Read the Excel file into a dictionary of DataFrames, with sheet names as keys
    excel_data = pd.read_excel(excel_file, sheet_name=None, engine="openpyxl")
    return excel_data


def get_excel_file(request):
    response = write_objects()
    return response


def create_bulk_student(df):
    try:
        # columns in Student sheet are : username, first name, last name, roll number, completed courses ids
        if df is not None:
            users_create = []
            users_update = []
            for _, row in df.iterrows():
                if CustomUser.objects.filter(username=row["username"]).exists():
                    user = CustomUser.objects.get(username=row["username"])
                    user.first_name = row["first name"]
                    user.last_name = row["last name"]
                    users_update.append(user)
                else:
                    user = CustomUser(
                        username=row["username"],
                        first_name=row["first name"],
                        last_name=row["last name"],
                    )
                    users_create.append(user)
            CustomUser.objects.bulk_create(
                users_create,
                ignore_conflicts=True,
            )
            CustomUser.objects.bulk_update(
                users_update, fields=["first_name", "last_name"]
            )
            message = "Students"
            for _, row in df.iterrows():
                if len(Student.objects.filter(roll_no=row["roll number"])) > 0:
                    student = Student.objects.get(roll_no=row["roll number"])
                    if str(row["completed courses ids"]) != "nan":
                        student.completed_courses.clear()
                        for course in str(row["completed courses ids"]).split(","):
                            course = Course.objects.get(course_code=course)
                            student.completed_courses.add(course)
                    student.save()
                else:
                    student = Student(
                        roll_no=row["roll number"],
                        user=CustomUser.objects.get(username=row["username"]),
                    )
                    if str(row["completed courses ids"]) != "nan":
                        student.save()
                        student.completed_courses.clear()
                        for course in str(row["completed courses ids"]).split(","):
                            student.completed_courses.add(course)
                    student.save()
        return True
    except:
        return False


def create_bulk_pod(df):
    # columns in POD sheet are : username, first name, last name, pod id
    try:
        if df is not None:
            users = []
            for _, row in df.iterrows():
                users.append(
                    CustomUser(
                        username=row["username"],
                        first_name=row["first name"],
                        last_name=row["last name"],
                    )
                )
            CustomUser.objects.bulk_create(users, ignore_conflicts=True)
            pods = []
            for _, row in df.iterrows():
                pod = POD(
                    user=CustomUser.objects.get(username=row["username"]),
                    pod_id=row["pod id"],
                )
                pods.append(pod)
            POD.objects.bulk_create(pods, ignore_conflicts=True)

            for pod in pods:
                if pod.pk is None:
                    print(pod)

        return True
    except:
        return False


def create_bulk_course(df):
    # columns in Course sheet are : course_code, course_name, term, course_type, status, active, description, level
    try:
        if df is not None:
            courses = []
            for _, row in df.iterrows():
                if str(row["course_code"]) != "nan":
                    courses.append(
                        Course(
                            course_code=row["course_code"],
                            course_name=row["course_name"],
                            description=row["description"],
                            level=row["level"],
                        )
                    )
            Course.objects.bulk_create(courses, ignore_conflicts=True)
        return True
    except:
        return False


def create_bulk_feedback(df):
    # columns in Feedback sheet are : scid, course code, feedback, rating, student roll number
    try:
        if df is not None:
            feedbacks = []
            for _, row in df.iterrows():
                if str(row["course code"]) != "nan":
                    course = Course.objects.get(course_code=row["course code"])
                    student = Student.objects.get(roll_no=row["student roll number"])
                    # now check if the feedback already exists
                    objs = Feedback.objects.filter(course=course, student=student)
                    if len(objs) > 0:
                        objs.first().delete()
                    feedback = Feedback(
                        course=Course.objects.get(course_code=row["course code"]),
                        title=row["title"],
                        description=row["description"],
                        rating=row["rating"],
                        student=Student.objects.get(roll_no=row["student roll number"]),
                    )
                    feedbacks.append(feedback)
            Feedback.objects.bulk_create(feedbacks, ignore_conflicts=True)
        return True
    except:
        return False


def write_objects():
    buffer = BytesIO()
    # creating 4 sheets in an excel file
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        # Student sheet
        # get all the student objects and put only username	first name	last name	roll number	completed courses ids in columns
        students = Student.objects.all()
        student_data = []
        for student in students:
            student_data.append(
                {
                    "username": student.user.username,
                    "first name": student.user.first_name,
                    "last name": student.user.last_name,
                    "roll number": student.roll_no,
                    "completed courses ids": ",".join(
                        [
                            course.course_code
                            for course in student.completed_courses.all()
                        ]
                    ),
                }
            )
        df = pd.DataFrame(
            student_data,
            columns=[
                "username",
                "first name",
                "last name",
                "roll number",
                "completed courses ids",
            ],
        )

        df.to_excel(writer, sheet_name="Student", index=False)
        # POD sheet
        # get all the pod objects and put only username	first name	last name	pod id in columns

        pods = POD.objects.all()
        pod_data = []
        for pod in pods:
            pod_data.append(
                {
                    "username": pod.user.username,
                    "first name": pod.user.first_name,
                    "last name": pod.user.last_name,
                    "pod id": pod.pod_id,
                }
            )

        df = pd.DataFrame(
            pod_data, columns=["username", "first name", "last name", "pod id"]
        )
        df.to_excel(writer, sheet_name="POD", index=False)
        # Course sheet
        # get all the course objects and put only course_code	course_name	term	course_type	status	active	description	level in columns
        courses = Course.objects.all()
        course_data = []
        for course in courses:
            course_data.append(
                {
                    "course_code": course.course_code,
                    "course_name": course.course_name,
                    "description": course.description,
                    "level": course.level,
                }
            )
        df = pd.DataFrame(
            course_data, columns=["course_code", "course_name", "description", "level"]
        )

        df.to_excel(writer, sheet_name="Course", index=False)
        # Feedback sheet
        # get all the feedback objects and put only	course code	feedback	rating	student roll number in columns
        feedbacks = Feedback.objects.all()
        feedback_data = []
        for feedback in feedbacks:
            feedback_data.append(
                {
                    "course code": feedback.course.course_code,
                    "title": feedback.title,
                    "description": feedback.description,
                    "rating": feedback.rating,
                    "student roll number": feedback.student.roll_no,
                }
            )

        df = pd.DataFrame(
            feedback_data,
            columns=[
                "course code",
                "title",
                "description",
                "rating",
                "student roll number",
            ],
        )
        df.to_excel(writer, sheet_name="Feedback", index=False)

    buffer.seek(0)

    # Save the buffer to a temporary file in the storage
    temp_file_name = default_storage.save(
        "temp_output.xlsx", ContentFile(buffer.getvalue())
    )

    # Create a response with the file for download
    response = HttpResponse(
        default_storage.open(temp_file_name).read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f"attachment; filename={temp_file_name}"

    # Clean up the temporary file
    default_storage.delete(temp_file_name)

    return response
