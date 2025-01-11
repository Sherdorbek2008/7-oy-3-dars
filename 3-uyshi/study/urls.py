from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name='home'),

    path("course/<int:course_id>/", course_detail, name='course_detail'),
    path("course/<int:course_id>/update", update_course, name='update_course'),
    path("course/<int:course_id>/delete", delete_course, name='delete_course'),
    path("course/add", add_course, name='add_course'),


    path("student/<int:student_id>/", student_detail, name='student_detail'),

    path('auth/register/', register, name='register'),
    path('auth/login/', loginView, name='login'),
    path('auth/logout/', logoutView, name='logout'),

    path('not-found/', not_found, name='not_found'),

    path('settings/', settings, name='settings'),
    path('settings/save/', settings, name='settings_save'),
    path('settings/photo/delete/', remove_picture, name='remove_picture'),
    path('settings/delete-account/', delete_account, name='delete_account'),
    path('settings/delete-account/confirm/', delete_account_confirm, name='delete_account_confirm'),

    path("send-mail/", send_email, name='email')

]
