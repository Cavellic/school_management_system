# Generated by Django 4.2.1 on 2023-07-26 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinsubject',
            name='grade',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentinsubject',
            name='mark',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentinsubject',
            name='remarks',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
