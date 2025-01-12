from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kurs nomini kiriting',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Kurs haqida ma'lumot kiriting",
                'rows': 4
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'name': 'Max 100 ta simvol bolishi shart!',
            'description': 'Matn 500 ta simvolgacha bo‘lishi mumkin.',
        }

        error_messages = {
            'name': {
                'max_length': 'Kurs nomi juda uzun! Max 100 ta simvol bo‘lishi kerak.',
                'required': 'Kurs nomi maydoni to‘ldirilishi shart.',
            },
            'description': {
                'max_length': 'Kurs tavsifi juda uzun! Max 500 ta simvol bo‘lishi kerak.',
                'required': 'Kurs tavsifi maydoni to‘ldirilishi shart.',
            },
            'photo': {
                'invalid': 'Fayl formati noto‘g‘ri! Iltimos, tasvir yuklang.',

            },
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        if 'description' in self.fields:
            self.fields['description'].initial = (
                "Kurs haqida ma'lumotlar:\n"
                "Davomiyligi:\n"
                "Kurs haqida nimalarni bilasiz?\n"
                "Kurs haqida ma'lumotlarni kiriting!"
            )


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismni kiriting',
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiyani kiriting',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "Elektron pochta manzilini kiriting",
            }),
            'course': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        help_texts = {
            'name': 'Ism uzunligi 100 ta simvoldan oshmasligi kerak!',
            'lastname': 'Familiya uzunligi 100 ta simvoldan oshmasligi kerak!',
            'email': 'To‘g‘ri formatda elektron pochta kiriting!',
            'course': 'Tanlov qiling: Kursni belgilang.',
        }
        error_messages = {
            'name': {
                'max_length': 'Ism juda uzun! Max 100 ta simvol bo‘lishi kerak.',
                'required': 'Ism maydoni to‘ldirilishi shart.',
            },
            'lastname': {
                'max_length': 'Familiya juda uzun! Max 100 ta simvol bo‘lishi kerak.',
                'required': 'Familiya maydoni to‘ldirilishi shart.',
            },
            'email': {
                'invalid': 'Elektron pochta formati noto‘g‘ri!',
                'required': 'Elektron pochta maydoni to‘ldirilishi shart.',
            },
            'course': {
                'invalid_choice': 'Tanlangan kurs mavjud emas!',
                'required': 'Kurs maydoni to‘ldirilishi shart.',
            },
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': "Foydalanuvchini ismi",
            'email': "Elektron pochta manzili",
            'password1': "Parolni kiriting",
            'password2': "Parolni qaytatdan kiriting"
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg', 'placeholder': 'Parolni kiriting'})
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg', 'placeholder': 'Parolni qaytatdan kiriting'})


class LoginForm(AuthenticationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username = self.fields['username']
        password = self.fields['password']

        username.label = "Foydalanuvchi nomi"
        username.widget.attrs.update({'class': "form-control form-control-lg"})
        password.widget.attrs.update({'class': "form-control form-control-lg"})




class EmailForm(forms.Form):
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control"
    }))

