# Generated by Django 4.2.1 on 2023-07-18 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('residential_address', models.CharField(blank=True, max_length=200, null=True)),
                ('postal_address', models.CharField(blank=True, max_length=200, null=True)),
                ('tel_number', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(choices=[('Boy', 'Boy'), ('Girl', 'Girl')], max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, max_length=10, null=True)),
                ('id_number', models.CharField(blank=True, max_length=20, null=True)),
                ('birth_entry_number', models.CharField(max_length=20)),
                ('guardian_first_name', models.CharField(max_length=100)),
                ('guardian_last_name', models.CharField(max_length=100)),
                ('guardian_residential_address', models.CharField(max_length=100)),
                ('guardian_postal_address', models.CharField(max_length=100)),
                ('home_tel', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('employer_name', models.CharField(max_length=100)),
                ('employer_tel', models.CharField(max_length=100)),
                ('position_held', models.CharField(max_length=100)),
                ('employer_address', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ClassLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_level', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EventsGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('body', models.TextField(blank=True, max_length=500, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('residential_address', models.CharField(blank=True, max_length=200, null=True)),
                ('postal_address', models.CharField(blank=True, max_length=200, null=True)),
                ('tel_number', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(choices=[('Boy', 'Boy'), ('Girl', 'Girl')], max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, max_length=10, null=True)),
                ('id_number', models.CharField(blank=True, max_length=20, null=True)),
                ('birth_entry_number', models.CharField(max_length=20)),
                ('guardian_first_name', models.CharField(max_length=100)),
                ('guardian_last_name', models.CharField(max_length=100)),
                ('guardian_residential_address', models.CharField(max_length=100)),
                ('guardian_postal_address', models.CharField(max_length=100)),
                ('home_tel', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('employer_name', models.CharField(max_length=100)),
                ('employer_tel', models.CharField(max_length=100)),
                ('position_held', models.CharField(max_length=100)),
                ('employer_address', models.CharField(max_length=100)),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.classlevel')),
            ],
        ),
        migrations.CreateModel(
            name='StudentClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='StudentInSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ec_number', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'M'), ('F', 'F')], max_length=20, null=True)),
                ('id_number', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.classlevel')),
                ('students', models.ManyToManyField(through='main.StudentInSubject', to='main.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='studentinsubject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subject'),
        ),
        migrations.CreateModel(
            name='StudentInClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.studentclass')),
            ],
        ),
        migrations.AddField(
            model_name='studentclass',
            name='class_teacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.teacher'),
        ),
        migrations.AddField(
            model_name='studentclass',
            name='students',
            field=models.ManyToManyField(through='main.StudentInClass', to='main.student'),
        ),
    ]
