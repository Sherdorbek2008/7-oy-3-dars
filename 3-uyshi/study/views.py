from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from .models import *
from django.core.mail import send_mail
from django.core.paginator import Paginator


def index(request: WSGIRequest):
    courses = Course.objects.all()
    students = Student.objects.all()
    course = Paginator(courses, 3)
    student = Paginator(students, 3)
    page = request.GET.get('page', 1)
    context = {
        "course": course.page(page),
        "students": student.page(page),
        "title": 'Bosh sahifa',
    }

    return render(request, "index.html", context)


@login_required
def course_detail(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk=course_id)
    students = Student.objects.filter(course_id=course_id)
    comments = Comment.objects.filter(course=course_id)
    form = CommentForm

    context = {
        "course": course,
        "students": students,
        "title": 'Bosh sahifa',
        "comments": comments,
        'form': form,
    }

    return render(request, "detail.html", context)


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
            form.save()
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
        form = CourseForm(data=request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumot muvaffaqiyatli o'zgartirildi!")
            return redirect('course_detail', course_id=course.id)
        else:
            messages.error(request, "Ma'lumotni o'zgartirishda xatolik yuz berdi.")
    else:
        form = CourseForm(instance=course)

    context = {
        'form': form,
        'course': course,
    }

    return render(request, 'add_course.html', context)


@permission_required('study.delete_course', login_url='not_found')
def delete_course(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    messages.success(request, "Ma'lumot muvaffaqiyatli o'chirildi!")
    return redirect('home')


@permission_required('study.add_student', login_url='not_found')
def add_student(request: WSGIRequest):
    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "O'quvchi muvaffaqiyatli qo'shildi!")
            return redirect('home')
        else:
            messages.error(request, "O'quvchi qo'shishda xatolik yuz berdi.")
    else:
        form = StudentForm()

    context = {
        "form": form
    }
    return render(request, 'add_student.html', context)


@permission_required('study.change_student', login_url='not_found')
def update_student(request: WSGIRequest, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = StudentForm(data=request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumot muvaffaqiyatli o'zgartirildi!")
            return redirect('student_detail', student_id=student.id)
        else:
            messages.error(request, "Ma'lumotni o'zgartirishda xatolik yuz berdi.")
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'student': student,
    }

    return render(request, 'add_student.html', context)


@permission_required('study.delete_student', login_url='not_found')
def delete_student(request: WSGIRequest, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    messages.success(request, "Ma'lumot muvaffaqiyatli o'chirildi!")
    return redirect('home')


def register(request: WSGIRequest):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tabriklayman, muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'auth/register.html', context)


def loginView(request: WSGIRequest):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request,
                             "Akkauntingizga muvaffaqiyatli kirdingiz. Endi barcha imkoniyatlardan foydalana olasiz.")
            return redirect('home')
    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'auth/login.html', context)


def logoutView(request: WSGIRequest):
    logout(request)
    messages.success(request, "Tizimdan chiqish muvaffaqiyatli amalga oshirildi.")
    return redirect('login')


def not_found(request):
    return render(request, '404.html')


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
