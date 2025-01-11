from django.core.exceptions import ValidationError
from .models import *


def Title(value):
    if Course.objects.filter(name=value).exists():
        raise ValidationError(
            "Kechirasiz, ushbu nom bilan kurs allaqachon ro'yxatdan o'tkazilgan. Iltimos, boshqa nom kiriting.")


def Description(value):
    valueLen = len(value)
    if valueLen > 1500:
        raise ValidationError("Matn uzunligi 1000 ta belgidan oshmasligi kerak.")
    elif valueLen < 5:
        raise ValidationError("Minimal 5 ta belgidan boshlanishi kerak.")


def registerName(value):
    if " " in value:
        raise ValidationError("Foydalanuvchi nomi yaroqsiz. Iltimos, qaytadan urunib ko'ring.")
