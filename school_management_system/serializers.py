from rest_framework import serializers
from django.contrib.auth.models import User
from school_management_system.models import School, Student


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.username = validated_data['email']
        user.save()
        return user


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class SignUpSerializer(serializers.Serializer):
    email = serializers.CharField()
    name = serializers.CharField()
    city = serializers.CharField()
    pin_code = serializers.IntegerField()
    password = serializers.CharField()


class AddStudentsSerializer(serializers.Serializer):
    bulk = serializers.BooleanField()
    grade = serializers.IntegerField()
    no_of_students = serializers.IntegerField()
    name = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    def validate_bulk(self, value):
        if value is True:
            if not self.initial_data.get('no_of_students'):
                raise serializers.ValidationError("''no_of_students' field is required for bulk create")
        elif value is False:
            if not self.initial_data.get('name'):
                raise serializers.ValidationError("'name' field is required for creating single student, 'password' is optional")
        return value

class EditStudentsSerializer(serializers.Serializer):
    student_no = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        if user and hasattr(user, "school") and not attrs.get('student_no'):
            raise serializers.ValidationError("'student_no' is required for school user")
        return attrs
