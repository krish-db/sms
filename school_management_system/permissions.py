from rest_framework.permissions import IsAuthenticated

class SchoolUser(IsAuthenticated):
    def has_permission(self, request, view):
        resp = super(SchoolUser, self).has_permission(request, view)
        return hasattr(request.user, "school") is True and resp

class StudentUser(IsAuthenticated):
    def has_permission(self, request, view):
        resp = super(StudentUser, self).has_permission(request, view)
        return hasattr(request.user, "student") is True and resp
