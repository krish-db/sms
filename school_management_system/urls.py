from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    path('signin/',
         jwt_views.TokenObtainPairView.as_view(),
         name ='token_obtain_pair'),
    path('signin/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name ='token_refresh'),
    path('students', views.AddorFilterStudents.as_view(), name='students'),
    path('students/edit', views.EditStudentDetails.as_view(), name='student_edit'),
]