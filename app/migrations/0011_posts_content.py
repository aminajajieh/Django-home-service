# Generated by Django 2.2.17 on 2021-02-08 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_clientservice_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='content',
            field=models.TextField(default='', verbose_name='وصف المقال'),
        ),
    ]