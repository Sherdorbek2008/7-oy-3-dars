from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name='home'),
    # course bilan bog'liq bo'lgan url lar
    path("course/<int:course_id>/", course_detail, name='course_detail'),
    path("course/<int:course_id>/update", update_course, name='update_course'),
    path("course/<int:course_id>/delete", delete_course, name='delete_course'),
    path("course/add", add_course, name='add_course'),

    # student bilan bog'liq bo'lgan url lar
    path("student/<int:student_id>/", student_detail, name='student_detail'),
    path("student/<int:student_id>/update", update_student, name='update_student'),
    path("student/<int:student_id>/delete", delete_student, name='delete_student'),
    path("student/add", add_student, name='add_student'),

    # authentificate
    path('auth/register/', register, name='register'),
    path('auth/login/', loginView, name='login'),
    path('auth/logout/', logoutView, name='logout'),

    path('not-found/', not_found, name='not_found'),

    path("send-mail/", send_email, name='email')

]
