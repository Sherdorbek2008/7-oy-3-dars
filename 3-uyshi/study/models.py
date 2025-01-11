from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)
    photo = models.ImageField(upload_to='users/photo', null=True, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['id']


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nomi')
    description = models.TextField(
        default="Kurs haqida:\ndavomiyligi:\n kurs haqida nimalarni bilasiz?",
        verbose_name="Tavsifi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kurs yaratilgan vaqti.")
    photo = models.ImageField(upload_to="course/photos", verbose_name='Rasmi', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'kurs'
        verbose_name_plural = 'kurslar'
        ordering = ['-created_at']


class Student(models.Model):
    name = models.CharField(max_length=150, verbose_name='Ismi')
    lastname = models.CharField(max_length=150, verbose_name='Familiyasi')
    email = models.EmailField(max_length=150, verbose_name="Elektron pochta manzili")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="qoshilgan vaqti")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Oqiyotgan kursi")

    def __str__(self):
        return f"{self.name} {self.lastname}"

    class Meta:
        verbose_name = "oquvchi"
        verbose_name_plural = "oquvchilar"
        ordering = ['-id']
