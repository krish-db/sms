from django.contrib import admin
from school_management_system.models import School, Student

class StudentAdmin(admin.ModelAdmin):
    list_filter = ('grade',)

# Register your models here.
admin.site.register(School)
admin.site.register(Student, StudentAdmin)
