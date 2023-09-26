from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length = 100, null=True, blank=True)
    body = models.TextField(max_length = 500, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

class StudentGallery(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

class EventsGallery(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

class ClassLevel(models.Model):
    class_level = models.CharField(max_length = 100)

    def __str__(self):
        return self.class_level

SEX = (
    ('Boy', 'Boy'),
    ('Girl', 'Girl'),
)
#applicants table
class Applicant(models.Model):
    first_name = models.CharField(max_length = 200, null=True, blank = True)
    last_name = models.CharField(max_length = 200, null=True, blank = True)
    residential_address = models.CharField(max_length = 200, null=True, blank = True)
    postal_address= models.CharField(max_length = 200, null=True, blank = True)
    tel_number = models.CharField(max_length = 20, null = True, blank = True)
    sex = models.CharField(max_length = 20, null = True, choices=SEX)
    date_of_birth = models.DateField(max_length = 10, null = True, blank = True)
    id_number = models.CharField(max_length = 20, null = True, blank = True)
    birth_entry_number = models.CharField(max_length = 20)
    guardian_first_name = models.CharField(max_length = 100)
    guardian_last_name = models.CharField(max_length = 100)
    guardian_residential_address = models.CharField(max_length = 100)
    guardian_postal_address = models.CharField(max_length = 100)
    home_tel = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    employer_name = models.CharField(max_length = 100)
    employer_tel = models.CharField(max_length = 100)
    position_held = models.CharField(max_length = 100)
    employer_address = models.CharField(max_length = 100)
    level = models.ForeignKey(ClassLevel, on_delete = models.CASCADE, null=True)
    status = models.IntegerField(default=0)
    applicant_file = models.FileField(blank=True, null = True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

GENDER = (
    ('M', 'M'),
    ('F', 'F'),
)

class Teacher(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.SET_NULL)
    ec_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, null=True, choices=GENDER)
    id_number = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        if self.gender == 'M':
            return 'Mr'+ ' ' + self.last_name
        else:
            return  'Ms' + ' ' + self.last_name


class Principal(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.SET_NULL)
    profile_pic = models.ImageField(default="logo.jpg",null=True, blank=True)

#applicants table

class Student(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.SET_NULL)
    profile_pic = models.ImageField(default="logo.jpg",null=True, blank=True)
    first_name = models.CharField(max_length = 200, null=True, blank = True)
    last_name = models.CharField(max_length = 200, null=True, blank = True)
    residential_address = models.CharField(max_length = 200, null=True, blank = True)
    postal_address= models.CharField(max_length = 200, null=True, blank = True)
    tel_number = models.CharField(max_length = 20, null = True, blank = True)
    sex = models.CharField(max_length = 20, null = True, choices=SEX)
    date_of_birth = models.DateField(max_length = 10, null = True, blank = True)
    id_number = models.CharField(max_length = 20, null = True, blank = True)
    birth_entry_number = models.CharField(max_length = 20)
    guardian_first_name = models.CharField(max_length = 100)
    guardian_last_name = models.CharField(max_length = 100)
    guardian_residential_address = models.CharField(max_length = 100)
    guardian_postal_address = models.CharField(max_length = 100)
    home_tel = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    employer_name = models.CharField(max_length = 100)
    employer_tel = models.CharField(max_length = 100)
    position_held = models.CharField(max_length = 100)
    employer_address = models.CharField(max_length = 100)
    level = models.ForeignKey(ClassLevel, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class StudentClass(models.Model):
    level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    class_teacher = models.ForeignKey(Teacher, null = True,blank=True, on_delete=models.SET_NULL)
    students = models.ManyToManyField(Student, through='StudentInClass')

    class Meta:
        unique_together = [['name', 'level', 'class_teacher']]

    def __str__(self):
        return str(self.level)+self.name

class StudentInClass(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = [['student', 'student_class']]

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name


class Subject(models.Model):
    name = models.CharField(max_length=100, null=True)
    teacher = models.ForeignKey(Teacher, null = True, on_delete=models.SET_NULL)
    level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through='StudentInSubject')

    def __str__(self):
        return self.name + ' ' + self.level.class_level

class StudentInSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    mark = models.PositiveIntegerField(max_length=3, null=True, blank=True)
    grade = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = [['student', 'subject']]

    def __str__(self):
        return self.subject.name



    



