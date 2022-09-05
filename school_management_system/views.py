from rest_framework.views import APIView
from school_management_system import serializers
from school_management_system.utils import created_response, general_error_response, success_response
from school_management_system.services import create_students, register_school, update_student_details
from school_management_system.permissions import SchoolUser, StudentUser


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
                success, msg = create_students(serializer.validated_data, request.user.school)
                if success:
                    return created_response('Successfully Created')
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
                    success, msg = update_student_details(serializer.validated_data, school)
                elif hasattr(request.user, "student"):
                    student = request.user.student
                    success, msg = update_student_details(serializer.validated_data, student=student)
                else:
                    success, msg = False, 'User is not a student nor a school'
                if success:
                    return success_response('Successfully Updated')
                else:
                    return general_error_response('Not Updated', msg)
            else:
                return general_error_response('Bad Parameters', serializer.errors)
        except Exception as exc:
            return general_error_response(str(exc))
