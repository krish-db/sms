from rest_framework.views import APIView
from school_management_system import serializers
from school_management_system.utils import created_response, general_error_response, success_response
from school_management_system.services import create_students, register_school, update_student_details
from school_management_system.permissions import SchoolUser, StudentUser
from django.db.models.query import QuerySet


class SignUp(APIView):
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                school = register_school(serializer.validated_data)
                return created_response(serializers.SchoolSerializer(school).data)
            else:
                return general_error_response('Bad Parameters', serializer.errors)
        except Exception as exc:
            return general_error_response(str(exc))


class AddorFilterStudents(APIView):
    permission_classes = (SchoolUser,)

    def get(self, request):
        try:
            grade = request.query_params.get('grade')
            queryset = request.user.school.students.all()
            if grade:
                queryset = queryset.filter(grade=grade)
            serializer = serializers.StudentSerializer(queryset, many=True)
            return success_response(serializer.data)
        except Exception as exc:
            return general_error_response(str(exc))

    def post(self, request):
        try:
            serializer = serializers.AddStudentsSerializer(data=request.data)
            if serializer.is_valid():
                created, msg = create_students(serializer.validated_data, request.user.school)
                if created:
                    many=True if isinstance(created, QuerySet) else False
                    student_serializer = serializers.StudentSerializer(created, many=many)
                    return created_response(student_serializer.data)
                else:
                    return general_error_response('Not Created', msg)
            else:
                return general_error_response('Bad Parameters', serializer.errors)
        except Exception as exc:
            return general_error_response(str(exc))

class EditStudentDetails(APIView):
    permission_classes = (SchoolUser|StudentUser,)

    def post(self, request):
        try:
            serializer = serializers.EditStudentsSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                if hasattr(request.user, "school"):
                    school = request.user.school
                    updated, msg = update_student_details(serializer.validated_data, school)
                elif hasattr(request.user, "student"):
                    student = request.user.student
                    updated, msg = update_student_details(serializer.validated_data, student=student)
                else:
                    updated, msg = False, 'User is not a student nor a school'
                if updated:
                    student_serializer = serializers.StudentSerializer(updated)
                    return success_response(student_serializer.data)
                else:
                    return general_error_response('Not Updated', msg)
            else:
                return general_error_response('Bad Parameters', serializer.errors)
        except Exception as exc:
            return general_error_response(str(exc))
