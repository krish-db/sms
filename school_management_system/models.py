from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class School(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=20)

    class Meta(object):
        db_table = 'school'
    
    def __str__(self):
        """Visual identification"""
        return self.name


class Student(models.Model):
    student_no = models.AutoField(db_column='student_id', primary_key=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, related_name='students')
    name = models.CharField(max_length=200, null=True, blank=True)
    grade = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])

    class Meta(object):
        db_table = 'student'
    
    def __str__(self):
        """Visual identification"""
        return str(self.student_no)
