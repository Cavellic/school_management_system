from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']



class ClassForm(ModelForm):
    class Meta:
        model = StudentClass
        fields = '__all__'
        exclude = ['students']

        widgets = {
            'level': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'class_teacher': forms.Select(attrs={'class': 'form-control'})
        }


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['students']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'})
        }

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['image', 'user']

        widgets = {
            'ec_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['profile_pic', 'user']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'residential_address': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_number': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_entry_number': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_residential_address': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_postal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'home_tel': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'employer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'employer_tel': forms.TextInput(attrs={'class': 'form-control'}),
            'position_held': forms.TextInput(attrs={'class': 'form-control'}),
            'employer_address': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
        }

class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        fields = '__all__'
        exclude = ['status',]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'residential_address': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_number': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_entry_number': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_residential_address': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_postal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'home_tel': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'employer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'employer_tel': forms.TextInput(attrs={'class': 'form-control'}),
            'position_held': forms.TextInput(attrs={'class': 'form-control'}),
            'employer_address': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'applicant_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ProfilePicForm(ModelForm):
    class Meta:
        model = Student
        fields = ('profile_pic',)

class principalProfilePicForm(ModelForm):
    class Meta:
        model = Principal
        fields = ('profile_pic',)


class StudentInSubjectForm(ModelForm):
    class Meta:
        model=StudentInSubject
        fields='__all__'

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

class StudentInClassForm(ModelForm):
    class Meta:
        model = StudentInClass
        fields='__all__'

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'student_class': forms.Select(attrs={'class': 'form-control'}),
        }


