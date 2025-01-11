from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from .forms import *



def index(request: WSGIRequest):
    course = Course.objects.all()
    students = Student.objects.all()

    context = {
        "courses": course,
        "students": students,
        "title": 'Bosh sahifa',
    }

    return render(request, "index.html", context)


@login_required
def course_detail(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk=course_id)
    students = Student.objects.filter(course_id=course_id)

    context = {
        "courses": [course],
        "students": students,
        "title": 'Bosh sahifa',
    }

    return render(request, "index.html", context)


@login_required
def student_detail(request: WSGIRequest, student_id):
    student = get_object_or_404(Student, pk=student_id)

    context = {
        "student": student,
    }

    return render(request, 'student.html', context)


@permission_required('study.add_course', login_url='not_found')
def add_course(request: WSGIRequest):
    if request.method == 'POST':
        form = CourseForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.create(Course)
            messages.success(request, "Kurs muvaffaqiyatli qo'shildi!")
            return redirect('home')
        else:
            messages.error(request, "Kurs qo'shishda xatolik yuz berdi.")
    else:
        form = CourseForm()

    context = {
        "form": form
    }
    return render(request, 'add_course.html', context)


@permission_required('study.change_course', login_url='not_found')
def update_course(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = CourseForm(data=request.POST)
        if form.is_valid():
            form.update(course)
            messages.success(request, "Ma'lumot muvaffaqiyatli o'zgartirildi!")
            return redirect('course_detail', course_id=course_id)

    form = CourseForm(initial={
        'title': course.name,
        'description': course.description,
        'photo': course.photo,
    })

    context = {
        'forms': form,
    }

    return render(request, 'add_course.html', context)


@permission_required('study.delete_course', login_url='not_found')
def delete_course(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()

    messages.success(request, "Ma'lumot muvaffaqiyatli o'chirildi!")
    return redirect('home')


def register(request: WSGIRequest):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.create(MyUser)
            messages.success(request, "Tabriklayman, muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'forms': form,
    }

    return render(request, 'auth/register.html', context)


def loginView(request: WSGIRequest):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                messages.error(request,
                               "Foydalanuvchi nomi yoki parol noto'g'ri kiritildi. Iltimos, ma'lumotlarni tekshirib qayta urinib ko'ring.")
            else:
                login(request, user)

                messages.success(request, "Tizimga muvaffaqiyatli kirdingiz.")
                return redirect('home')
    else:
        form = LoginForm()

    context = {
        'forms': form
    }

    return render(request, 'auth/login.html', context)


def logoutView(request: WSGIRequest):
    logout(request)

    messages.success(request, "Tizimdan chiqish muvaffaqiyatli amalga oshirildi.")
    return redirect('login')


def not_found(request):
    return render(request, '404.html')


def settings(request: WSGIRequest):
    user = get_object_or_404(MyUser, username=request.user.username)
    if request.method == 'POST':
        form = SettingsForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():

            form.save()

            messages.success(request, "Ma'lumotlar muvaffaqiyatli saqlandi.")
            return redirect('settings_save')

    else:
        form = SettingsForm(instance=user)

    context = {
        'forms': form,
        'current_year': datetime.now().year
    }

    return render(request, 'settings.html', context)


def remove_picture(request: WSGIRequest):
    user = request.user

    if user.photo:
        user.photo = None
        user.save()

        messages.success(request, "Profil rasmingiz o'chirildi.")
    else:
        messages.error(request, "Sizda profil rasm mavjud emas!")

    return redirect('settings')



def delete_account(request):
    return render(request, 'delete_account.html')



def delete_account_confirm(request: WSGIRequest):
    user = request.user
    user.delete()

    messages.success(request, "Hisobingiz muvaffaqiyatli o'chirildi.")
    return redirect('index')


def not_found(request):
    context = {
        'current_year': datetime.now().year
    }

    return render(request, '404.html', context)

def send_email(request: WSGIRequest):
    if request.method == "POST":
        form = EmailForm(data=request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            users = MyUser.objects.all()
            for user in users:
                send_mail(
                    subject,
                    message,
                    "madrahimovq@gmail.com",
                    [user.email],
                    fail_silently=False)
            messages.success(request, "Xamma foydalanuvchilarga email habaringiz yuborildi!")
            return redirect('home')
        else:
            print(form.errors)

    else:
        form = EmailForm()
    context = {
        "form": form
    }
    return render(request, "send_email.html", context)
