# Generated by Django 2.2.17 on 2021-02-06 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'نوع خدمه', 'verbose_name_plural': 'انواع الخدمات'},
        ),
        migrations.AlterField(
            model_name='bond',
            name='id',
            field=models.AutoField(max_length=100, primary_key=True, serialize=False, verbose_name='رقم الاذن'),
        ),
    ]
