# Generated by Django 4.2.1 on 2023-07-29 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_studentclass_level_alter_studentinsubject_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
