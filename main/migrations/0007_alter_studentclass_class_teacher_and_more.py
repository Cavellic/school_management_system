# Generated by Django 4.2.1 on 2023-07-26 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_studentclass_class_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentclass',
            name='class_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='studentclass',
            unique_together={('name', 'class_teacher')},
        ),
    ]
