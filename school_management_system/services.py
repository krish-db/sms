from school_management_system.models import School, Student
from django.contrib.auth.models import User
from django.db import transaction
from school_management_system import serializers


def create_and_assing_user_for_student(student, password=None):
    user = User.objects.create(username=student.student_no)
    if not password:
        password = 'Password'+str(student.student_no)
    user.set_password(password)
    user.save()
    student.user = user
    student.save()

def create_students(validated_data, school):
    try:
        if validated_data.get('bulk'):
            no_of_students = validated_data.get('no_of_students')
            grade = validated_data.get('grade')
            with transaction.atomic():
                students = [Student(grade=grade, school=school) for n in range(0, no_of_students)]
                students = Student.objects.bulk_create(students)
                students_qs = school.students.filter(grade=grade).order_by('-student_no')[:no_of_students]
                for student in students_qs:
                    create_and_assing_user_for_student(student)
                return students_qs, None
        else:
            with transaction.atomic():
                student = Student.objects.create(name=validated_data.get('name'),
                                    school=school,
                                    grade=validated_data.get('grade'))
                password = validated_data.get('password', None)
                create_and_assing_user_for_student(student, password)
            return student, None
    except Exception as exc:
        return False, str(exc)

def register_school(validated_data):
    with transaction.atomic():
        user_serializer = serializers.UserCreateSerializer(data=validated_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            validated_data.pop('password')
        school = School.objects.create(user=user, **validated_data)
        return school

def update_student_details(validated_data, school=None, student=None):
    student_no = validated_data.get('student_no')
    name = validated_data.get('name')
    password = validated_data.get('password')
    with transaction.atomic():
        if not student and school:
            student = school.students.filter(student_no=student_no).last()
        if student:
            if name:
                student.name = name
                student.save()
            if password:
                user = student.user
                user.set_password(password)
                user.save()
                return student, None
        else:
            return False, 'Student Not Found with student_no' + str(student_no)
