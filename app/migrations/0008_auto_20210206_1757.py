# Generated by Django 2.2.17 on 2021-02-06 15:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210206_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientservice',
            name='date1',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='تاريخ بداية الخدمه'),
        ),
        migrations.AlterField(
            model_name='clientservice',
            name='date2',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='تاريخ نهاية الخدمه'),
        ),
    ]
