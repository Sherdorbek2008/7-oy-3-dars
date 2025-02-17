# Generated by Django 5.1.4 on 2025-01-06 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['-id'], 'verbose_name': 'oquvchi', 'verbose_name_plural': 'oquvchilar'},
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(default='Kurs haqida:\ndavomiyligi:\n kurs haqida nimalarni bilasiz?', verbose_name='Tavsifi'),
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.course', verbose_name='Oqiyotgan kursi'),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=150, verbose_name='Elektron pochta manzili'),
        ),
        migrations.AlterField(
            model_name='student',
            name='enrolled_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='qoshilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='student',
            name='lastname',
            field=models.CharField(max_length=150, verbose_name='Familiyasi'),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Ismi'),
        ),
    ]
