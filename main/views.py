from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import StudentFilter
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import datetime

from .functions import *
from .decorators import *
from .models import *
from .forms import *
import socket


# Create your views here.
def home(request):
    news = News.objects.all()
    context = {'news': news}

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        subject = subject
        message = f'{message}'
        email_from = email
        recipient_list = [settings.EMAIL_HOST_USER]

        try:
            if name and email and subject and message != "":
                send_mail(subject, message, email_from,
                        recipient_list, fail_silently=False)
                messages.success(
                request, ("Your email has been sent successfully \n we will get back to you as soon as we can"))
                return redirect("home")
            else:
                messages.error(
                    request, ("Enter all the required info")
                )

        except socket.gaierror as e:
            messages.error(
                request, ("Message not sent")
            )
            return redirect('home')

        
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html')

def subjects(request):
    return render(request, 'main/subjects.html')

def admission(request):
    return render(request, 'main/admission.html')

def feespayment(request):
    return render(request, 'main/feespayment.html')

# function to save applicants details
def onlineApp(request):
    form = ApplicantForm()
    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES )
        if form.is_valid():
            form.save()
            return redirect('onlineApp')
        
    context={'form':form}
    return render(request, 'main/onlineApp.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        subject = subject
        message = f'{message}'
        email_from = email
        recipient_list = [settings.EMAIL_HOST_USER]
        try:
            send_mail(subject, message, email_from,
                      recipient_list, fail_silently=False)
            messages.success(request, ("Done"))
        except socket.gaierror as e:
            messages.info(
                request, ("Fill all the requirements")
            )
    return render(request, 'main/contact.html')

def staffGallery(request):
    images = Image.objects.all()
    context = {'images': images}
    return render(request, 'main/staffGallery.html', context)

def studentGallery(request):
    students = StudentGallery.objects.all()
    context = {'students': students}
    return render(request, 'main/studentsGallery.html', context)

def eventsGallery(request):
    events = EventsGallery.objects.all()
    context = {'events': events}
    return render(request, 'main/eventsGallery.html', context)

def receptionistDashboard(request):
    return render(request, 'dashboard/baseReceptionistDashboard.html')

@login_required
@admin_only
def student_application_approval(request, id):
    
    student = Applicant.objects.get(id=id)
    student.status = 1
    student.save()
    messages.success(
        request, ("Application has been approved"))

    approved_application = Student(first_name=student.first_name, last_name=student.last_name, residential_address=student.residential_address, postal_address=student.postal_address, tel_number=student.tel_number, sex=student.sex, date_of_birth=student.date_of_birth, id_number=student.id_number, birth_entry_number=student.birth_entry_number, guardian_first_name=student.guardian_first_name,
                              guardian_last_name=student.guardian_last_name, guardian_residential_address=student.guardian_residential_address, guardian_postal_address=student.guardian_postal_address, home_tel=student.home_tel, email=student.email, employer_name=student.employer_name, employer_tel=student.employer_tel, position_held=student.position_held, employer_address=student.employer_address)
    approved_application.save()
    return redirect('onlineApplications')

@login_required
@admin_only
def student_application_decline(request, id):
    student_approval = Applicant.objects.get(id=id)
    student_approval.status = 2
    student_approval.save()
    messages.error(
        request, ("Application has been rejected"))
    return redirect('onlineApplications')

@login_required
@admin_only
def deleteStudent(request, pk):
    student = Student.objects.get(id=pk)
    student_classes = StudentClass.objects.all()
    if request.method == 'POST':
        student.delete()
        return redirect('viewStudents')
    context = {'student': student, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/deleteStudent.html', context)

@login_required
@admin_only
def studentInfo(request, pk):
    student_classes = StudentClass.objects.all()
    student = Student.objects.get(id=pk)
    subjects = student.subject_set.all()
    context = {'student': student, 'subjects': subjects, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/studentInfo.html', context)

@login_required
@admin_only
def approveApplication(request, pk):
    student_classes = StudentClass.objects.all()
    applicant = Applicant.objects.get(id=pk)
    context = {'applicant': applicant,'student_classes':student_classes }

    return render(request, 'dashboard/principalDashboard/applicationConfirmation.html', context)

def rejectApplication(request, pk):
    student_classes = StudentClass.objects.all()
    applicant = Applicant.objects.get(id=pk)
    context = {'applicant': applicant,'student-classes':student_classes }

    return render(request, 'dashboard/principalDashboard/rejectApplication.html', context)

@login_required
@admin_only
def onlineApplications(request):
    student_classes = StudentClass.objects.all()
    applicants = Applicant.objects.all()

    pending = []

    for applicant in applicants:
        if applicant.status == 0:
            pending.append(applicant)

    pending_applications = len(pending)

    if pending_applications > 0:
        p_applications = pending_applications
    else:
        p_applications = ''

    context = {'applicants': applicants, 'pending_applications': pending_applications,
               'p_applications': p_applications,'student_classes':student_classes }
    return render(request, 'dashboard/principalDashboard/onlineApplications.html', context)

@login_required
@admin_only
def applicantInfo(request, pk):
    student_classes = StudentClass.objects.all()
    applicant = Applicant.objects.get(id=pk)
    context={'applicant': applicant, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/applicantInfo.html', context )

# Admin and the methods
@login_required
@admin_only
def adminDashboard(request):
    applicants = Applicant.objects.all()
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    all_students = students.count()
    all_teachers = teachers.count()
    principal = request.user.principal

    student_classes = StudentClass.objects.all()

    pending = []
    approved = []
    declined = []

    for applicant in applicants:
        if applicant.status == 0:
            pending.append(applicant)
        elif applicant.status == 1:
            approved.append(applicant)
        else:
            declined.append(applicant)

    approved_applications = len(approved)
    pending_applications = len(pending)
    declined_applications = len(declined)

    if pending_applications > 0:
        p_applications = pending_applications
    else:
        p_applications = ''

    context = {
        'applicants': applicants,
        'all_students': all_students,
        'all_teachers': all_teachers,
        'approved_applications': approved_applications,
        'pending_applications': pending_applications,
        'declined_applications': declined_applications,
        'p_applications': p_applications,
        'student_classes': student_classes,
        'principal': principal
    }
    return render(request, 'dashboard/principalDashboard/index.html', context)

# function to register new student
@login_required
@admin_only
def studentRegistration(request):
    student_classes = StudentClass.objects.all()
    form = StudentForm()

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewStudents')

    context = {'form':form, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/studentReg.html', context)

@login_required
@admin_only
def updateStudent(request, pk):
    student_classes = StudentClass.objects.all()
    student = Student.objects.get(id=pk)
    form =StudentForm(instance=student)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('viewStudents')
    context = {'form':form, 'student_classes': student_classes}
    return render(request, 'dashboard/principalDashboard/studentReg.html', context)


@login_required
@admin_only
def viewStudents(request):
    student_classes = StudentClass.objects.all()
    students = Student.objects.all()
    all_students = students.count()
    myFilter = StudentFilter(request.GET, queryset=students)
    students = myFilter.qs

    page = request.GET.get('page')
    number_of_items = 4
    paginator = Paginator(students, number_of_items)

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        page=1
        students = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        students = paginator.page(page) 

    context = {
        'students': students,
        'all_students': all_students,
        'myFilter': myFilter,
        'page':page,
        'paginator':paginator,
        'student_classes':student_classes
    }
    return render(request, 'dashboard/principalDashboard/viewStudents.html', context)

@login_required
@admin_only
def addTeacher(request):
    student_classes = StudentClass.objects.all()
    form = TeacherForm()

    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_teachers')

    context = {'form': form, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/addTeacher.html', context)

@login_required
@admin_only
def all_teachers(request):
    student_classes = StudentClass.objects.all()
    teachers = Teacher.objects.all()

    context = {'teachers': teachers,'student_classes':student_classes }
    return render(request, 'dashboard/principalDashboard/all_teachers.html', context)

@login_required
@admin_only
def teacherInfo(request, pk):
    student_classes = StudentClass.objects.all()
    teacher = Teacher.objects.get(id=pk)
    subjects = teacher.subject_set.all()

    context = {'teacher': teacher, 'subjects': subjects, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/teacherInfo.html', context)

@login_required
@admin_only
def updateTeacher(request, pk):
    student_classes = StudentClass.objects.all()
    teacher = Teacher.objects.get(id=pk)
    form = TeacherForm(instance=teacher)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('all_teachers')
    context = {'form':form, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/addTeacher.html', context)


@login_required
@admin_only
def deleteTeacher(request,pk):
    student_classes = StudentClass.objects.all()
    teacher = Teacher.objects.get(id=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('all_teachers')
        messages.success(
            request, 'Teacher has been successfully deleted'
        )
    context = {'teacher': teacher, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/deleteTeacher.html', context)

@login_required
@admin_only
def addClass(request):
    student_classes = StudentClass.objects.all()
    form = ClassForm()

    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewClasses')

    context = {'form': form, 'student-classes':student_classes}
    return render(request, 'dashboard/principalDashboard/addClass.html', context)

@login_required
@admin_only
def updateClass(request, pk):
    student_classes = StudentClass.objects.all()
    clas = StudentClass.objects.get(id=pk)
    form = ClassForm(instance=clas)

    if request.method == 'POST':
        form = ClassForm(request.POST, instance = clas)
        if form.is_valid():
            form.save()
            return redirect('viewClasses')
    context = {'form':form, 'clas':clas, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/addClass.html', context)

@login_required
@admin_only
def deleteClass(request, pk):
    student_classes = StudentClass.objects.all()
    clas = StudentClass.objects.get(id=pk)
    if request.method == 'POST':
        clas.delete()
        return redirect('viewClasses')
        messages.success(
            request, 'Class has been successfully deleted'
        )
    context = {'clas': clas, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/deleteClass.html', context)

@login_required
@admin_only
def addSubject(request):
    student_classes = StudentClass.objects.all()
    form = SubjectForm()

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewSubject')

    context = {'form': form, 'student_classes':student_classes}

    return render(request, 'dashboard/principalDashboard/addSubject.html', context)

@login_required
@admin_only
def updateSubject(request, pk):
    student_classes = StudentClass.objects.all()
    subject = Subject.objects.get(id=pk)
    form = SubjectForm(instance=subject)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(
            request, 'Subject has been successfully updated'
        )
            return redirect('viewSubject')
            

    context = {'form':form, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/addSubject.html', context)

@login_required
@admin_only
def deleteSubject(request, pk):
    student_classes = StudentClass.objects.all()
    subject = Subject.objects.get(id=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('viewSubject')
        messages.success(
            request, 'Subject has been successfully deleted'
        )
    context = {'subject': subject, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/deleteSubject.html', context)

@login_required
@admin_only
def classInfo(request, pk):
    classes = StudentClass.objects.get(id=pk)
    students = classes.students.all()
    student_classes = StudentClass.objects.all()
    context = {'classes': classes, 'students': students, 'student_classes':student_classes }
    return render(request, 'dashboard/principalDashboard/classInfo.html', context)

@login_required
@admin_only
def viewClasses(request):
    student_classes = StudentClass.objects.all()
    classes = StudentClass.objects.all()
    context = {'classes': classes, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/viewClasses.html', context)

@login_required
@admin_only
def viewSubject(request):
    student_classes = StudentClass.objects.all()
    subjects = Subject.objects.all()
    context = {'subjects':subjects,'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/viewSubjects.html', context)

@login_required
@admin_only
def reportCard(request, pk):
    student_classes = StudentClass.objects.all()
    student=Student.objects.get(id=pk)
    subjects = student.studentinsubject_set.all()
    for subject in subjects:
        if subject.mark:
            if student.level == 'Form 5' or 'Form 6':
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Excellent'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Very Good'

                elif subject.mark >=55 and subject.mark <=64:
                    subject.grade = 'C'
                    subject.remarks = 'Pass With Credit'

                elif subject.mark >=45 and subject.mark <= 54:
                    subject.grade = 'D'
                    subject.remarks = 'Pass'
                
                elif subject.mark >=40 and subject.mark <= 44:
                    subject.grade = 'E'
                    subject.remarks = 'Pass'

                elif subject.mark >=35 and subject.mark <=39:
                    subject.grade = 'O'
                    subject.remarks = 'Subsidiary'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'
            else:
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Distinction'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Excellent'

                elif subject.mark >=55 and subject.mark <= 64:
                    subject.grade = 'C'
                    subject.remarks = 'Good'

                elif subject.mark >=45 and subject.mark <=54:
                    subject.grade = 'D'
                    subject.remarks = 'Average'

                elif subject.mark >=35 and subject.mark <=44:
                    subject.grade = 'E'
                    subject.remarks = 'Below Average'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'

    context={'student':student, 'subjects':subjects, 'student_classes':student_classes}
    return render(request, 'dashboard/principalDashboard/reportCard.html', context)

@login_required
@admin_only
def principalAccountSettings(request):
    form = principalProfilePicForm(instance=request.user.principal)
    if request.method == 'POST':
        form = principalProfilePicForm(request.POST, request.FILES, instance=request.user.principal)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'dashboard/principalDashboard/accountSettings.html', context)

def allStudentsPdf(request):
    student_classes = StudentClass.objects.all()
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename=main' +\
        str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    student = request.user.student
    subjects = request.user.student.studentinsubject_set.all()
    
    for subject in subjects:
        if subject.mark:
            if student.level == 'Form 5' or 'Form 6':
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Excellent'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Very Good'

                elif subject.mark >=55 and subject.mark <=64:
                    subject.grade = 'C'
                    subject.remarks = 'Pass With Credit'

                elif subject.mark >=45 and subject.mark <= 54:
                    subject.grade = 'D'
                    subject.remarks = 'Pass'
                
                elif subject.mark >=40 and subject.mark <= 44:
                    subject.grade = 'E'
                    subject.remarks = 'Pass'

                elif subject.mark >=35 and subject.mark <=39:
                    subject.grade = 'O'
                    subject.remarks = 'Subsidiary'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'
            else:
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Distinction'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Excellent'

                elif subject.mark >=55 and subject.mark <= 64:
                    subject.grade = 'C'
                    subject.remarks = 'Good'

                elif subject.mark >=45 and subject.mark <=54:
                    subject.grade = 'D'
                    subject.remarks = 'Average'

                elif subject.mark >=35 and subject.mark <=44:
                    subject.grade = 'E'
                    subject.remarks = 'Below Average'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'

    html_string = render_to_string(
        'dashboard/studentDashboard/reportPdf.html',
        {'student':student, 'subjects':subjects, 'student_classes':student_classes}
    )
    html=HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output=open(output.name, 'rb')
        response.write(output.read())

    return response


@login_required(login_url='loginStudent')
@allowed_users(allowed_roles=['student'])
def studentDashboard(request):
    student = request.user.student
    subjects = request.user.student.subject_set.all()
    context = {
        'subjects': subjects
    }
    return render(request, 'dashboard/studentDashboard/index.html', context)

@login_required(login_url='loginStudent')
@allowed_users(allowed_roles=['student'])
def mySubjects(request):
    student = request.user.student
    subjects = request.user.student.studentinsubject_set.all()
    context = {
        'subjects': subjects
    }
    return render(request, 'dashboard/studentDashboard/mySubjects.html', context)

@login_required(login_url='loginStudent')
@allowed_users(allowed_roles=['student'])
def myResults(request):
    student = request.user.student
    subjects = request.user.student.studentinsubject_set.all()
    context = {
        'subjects':subjects
    }
    for subject in subjects:
        if subject.mark:
            if student.level == 'Form 5' or 'Form 6':
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Excellent'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Very Good'

                elif subject.mark >=55 and subject.mark <=64:
                    subject.grade = 'C'
                    subject.remarks = 'Pass With Credit'

                elif subject.mark >=45 and subject.mark <= 54:
                    subject.grade = 'D'
                    subject.remarks = 'Pass'
                
                elif subject.mark >=40 and subject.mark <= 44:
                    subject.grade = 'E'
                    subject.remarks = 'Pass'

                elif subject.mark >=35 and subject.mark <=39:
                    subject.grade = 'O'
                    subject.remarks = 'Subsidiary'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'
            else:
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Distinction'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Excellent'

                elif subject.mark >=55 and subject.mark <= 64:
                    subject.grade = 'C'
                    subject.remarks = 'Good'

                elif subject.mark >=45 and subject.mark <=54:
                    subject.grade = 'D'
                    subject.remarks = 'Average'

                elif subject.mark >=35 and subject.mark <=44:
                    subject.grade = 'E'
                    subject.remarks = 'Below Average'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'
    return render(request, 'dashboard/studentDashboard/myResults.html', context)

@login_required(login_url='loginStudent')
@allowed_users(allowed_roles=['student'])
def studentAccountSettings(request):
    form = ProfilePicForm(instance=request.user.student)
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=request.user.student)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'dashboard/studentDashboard/accountSettings.html', context)

def updateAccount(request):
    
    return render(request, 'dashboard/studentDashboard/accountSettings.html')

@login_required(login_url='loginStudent')
@allowed_users(allowed_roles=['student'])
def studentReportPdf(request):
    student = request.user.student
    subjects = request.user.student.studentinsubject_set.all()
    context = {
        'subjects':subjects,
        'student': student
    }
    for subject in subjects:
        if subject.mark:
            if student.level == 'Form 5' or 'Form 6':
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Excellent'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Very Good'

                elif subject.mark >=55 and subject.mark <=64:
                    subject.grade = 'C'
                    subject.remarks = 'Pass With Credit'

                elif subject.mark >=45 and subject.mark <= 54:
                    subject.grade = 'D'
                    subject.remarks = 'Pass'
                
                elif subject.mark >=40 and subject.mark <= 44:
                    subject.grade = 'E'
                    subject.remarks = 'Pass'

                elif subject.mark >=35 and subject.mark <=39:
                    subject.grade = 'O'
                    subject.remarks = 'Subsidiary'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'
            else:
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Distinction'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Excellent'

                elif subject.mark >=55 and subject.mark <= 64:
                    subject.grade = 'C'
                    subject.remarks = 'Good'

                elif subject.mark >=45 and subject.mark <=54:
                    subject.grade = 'D'
                    subject.remarks = 'Average'

                elif subject.mark >=35 and subject.mark <=44:
                    subject.grade = 'E'
                    subject.remarks = 'Below Average'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'
    template_path = 'dashboard/studentDashboard/reportPdf.html'
    response = HttpResponse(content_type='application/pdf')
    #if you want to download:
    #response['Content-Disposition'] = 'attachment; file_name = "myResults.html" '
    #if you want to view:
    response['Content-Disposition'] = 'file_name = "myResults.html" '
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response
    )

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teacherDashboard(request):

    teacher = request.user.teacher
    
    subject = request.user.teacher.subject_set.all()
    
    classs = request.user.teacher.studentclass_set.all()
    context = {
        'teacher':teacher,
        'classs':classs,
        'subject':subject,
    }

    return render(request, 'dashboard/teacherDashboard/index.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teacherClass(request,pk):
    subject = request.user.teacher.subject_set.all()
    
    classs = request.user.teacher.studentclass_set.all()
    classs = request.user.teacher.studentclass_set.all()
    stud_class=classs[0]
    students=classs[0].students.all()

    context={
        'students':students,
        'stud_class':stud_class,
        'classs':classs,
        'subject':subject,
    }
    clas = StudentClass.objects.get(id=pk)
    student = Student.objects.all()

    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            for stud in student.all():
                if stud.id == int(id):
                    student1 = Student.objects.get(id=id)
                    if student1 in clas.students.all():
                        messages.info(
                            request, f'{student1} is already in {clas}'
                        )
                    else:
                        if student1.level == clas.level:
                            clas.students.add(student1)
                            messages.success(
                                request, f'{student1.first_name} has been successfully added in {clas}'
                            )
                        else:
                            messages.info(
                                request, f'You cant add a {student1.level} student in {clas.level}'
                            )
    except ValueError:
        messages.info(
                        request, 'Input Student Reg No.'
                    )
        print("No data")
     
    return render(request, 'dashboard/teacherDashboard/teacherClass.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def removeStudentFromClass(request, pk):
    subject = request.user.teacher.subject_set.all()
    
    classs = request.user.teacher.studentclass_set.all()
    stud_class=classs[0]
    students=classs[0].students.all()

    context={
        'students':students,
        'stud_class':stud_class,
        'subject': subject,
        'classs':classs
    }
    clas = StudentClass.objects.get(id=pk)
    student = Student.objects.all()

    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            for stud in clas.students.all():
                if stud.id == int(id):
                    student1 = Student.objects.get(id=id)
                    clas.students.remove(student1)
                    messages.success(
                        request, f'Student {stud.first_name} has been removed from {clas}.'
                    )
                    break

    except ValueError:
        messages.info(
                        request, 'Input Student Reg No.'
                    )
        print("No data")
    return render(request, 'dashboard/teacherDashboard/removeStudentFromClass.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def removeStudentFromSubject(request, pk):
    subject = request.user.teacher.subject_set.all()
    
    classs = request.user.teacher.studentclass_set.all()
    sub = Subject.objects.get(id=pk)
    subject_students = sub.students.all()
    student = Student.objects.all()
    context={
        'subject': subject,
        'student':student, 
        'subject_students':subject_students,
        'sub':sub,
        'classs':classs,
        }

    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            print('Id', id)
            for stud in subject_students.all():
                if stud.id == int(id):
                    student1 = Student.objects.get(id=id)
                    sub.students.remove(student1)
                    messages.success(
                        request, f'Student {stud.first_name} has been removed from {sub.name}.'
                    )
                    print("Wow")
                    break
    
    except ValueError:
        messages.info(
            request, 'Input Student Reg No.'
            )
        print("No data")
    
    return render(request, 'dashboard/teacherDashboard/removeStudentFromSubject.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def studentReportCard(request, pk):
    subject = request.user.teacher.subject_set.all()
    classs = request.user.teacher.studentclass_set.all()

    student = Student.objects.get(id=pk)
    subjects = student.studentinsubject_set.all()

    context = {'student':student, 'subjects':subjects, 'subject':subject, 'classs':classs}

    for subject in subjects:
        if subject.mark:
            if student.level == 'Form 5' or 'Form 6':
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Excellent'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Very Good'

                elif subject.mark >=55 and subject.mark <=64:
                    subject.grade = 'C'
                    subject.remarks = 'Pass With Credit'

                elif subject.mark >=45 and subject.mark <= 54:
                    subject.grade = 'D'
                    subject.remarks = 'Pass'
                
                elif subject.mark >=40 and subject.mark <= 44:
                    subject.grade = 'E'
                    subject.remarks = 'Pass'

                elif subject.mark >=35 and subject.mark <=39:
                    subject.grade = 'O'
                    subject.remarks = 'Subsidiary'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'
            else:
                if subject.mark >=75 and subject.mark <= 100:
                    subject.grade = 'A'
                    subject.remarks = 'Distinction'

                elif subject.mark >=65 and subject.mark <=74:
                    subject.grade = 'B'
                    subject.remarks = 'Excellent'

                elif subject.mark >=55 and subject.mark <= 64:
                    subject.grade = 'C'
                    subject.remarks = 'Good'

                elif subject.mark >=45 and subject.mark <=54:
                    subject.grade = 'D'
                    subject.remarks = 'Average'

                elif subject.mark >=35 and subject.mark <=44:
                    subject.grade = 'E'
                    subject.remarks = 'Below Average'

                else:
                    subject.grade = 'U'
                    subject.remarks = 'Fail'

    return render(request, 'dashboard/teacherDashboard/studentReportCard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def subjectInfo(request, pk):
    subject = request.user.teacher.subject_set.all()
    
    classs = request.user.teacher.studentclass_set.all()
    sub = Subject.objects.get(id=pk)
    subject_students = sub.students.all()
    student = Student.objects.all()
    context={'sub': sub,
    'student':student, 
    'subject_students':subject_students,
    'subject':subject,
    'classs':classs
    }

    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            for stud in student:
                if stud.id == int(id):
                    student1 = Student.objects.get(id=id)
                    if student1 in sub.students.all():
                        messages.info(
                            request, f'{student1.first_name} is already in {sub.name}'
                        )
                    else:
                        if student1.level == subject.level:
                            subject.students.add(student1)
                            messages.success(
                                request, student1.first_name + " has been successfully added to "+str(sub.level) +' '+ subject.name
                            )
                        else:
                            messages.info(
                                request, "You can't add a " + str(student1.level) + " student into a " + str(subject.level) + " subject"
                                )
    except ValueError:
        messages.info(
            request, 'Input Student Reg No. to proceed'
        )
    
    return render(request, 'dashboard/teacherDashboard/subjectInfo.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def subjectStudents(request, pk):
    subject = request.user.teacher.subject_set.all()
    classs = request.user.teacher.studentclass_set.all()

    sub = Subject.objects.get(id=pk)
    subject_students = sub.students.all()
    context={
        'sub':sub,
        'subject_students':subject_students,
        'subject':subject,
        'classs':classs
    }
    return render(request, 'dashboard/teacherDashboard/subjectStudents.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def updateResults(request, pk):
    student_subject = StudentInSubject.objects.get(id=pk)
    if request.method == 'POST':
        student_subject.subject.name = request.POST.get('subject')
        student_subject.mark = request.POST.get('exam_mark')

        student_subject.save()

    context={'student_subject':student_subject}
    return render(request, 'dashboard/teacherDashboard/updateResults.html', context)

@unauthenticated
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
        else:
            return HttpResponse('Invalid username or password')

    return render(request, 'main/login.html')

@unauthenticated
def loginStudent(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
        else:
            return HttpResponse('Invalid username or password')

    return render(request, 'main/studentLogin.html')

@unauthenticated
def userRegister(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='teacher')
            user.groups.add(group)
            ec_number=request.POST.get('id')
            
            teacher=Teacher.objects.get(ec_number=ec_number)
            teacher.user=user
            teacher.save()

            messages.success(request, 'Account for '+username+ ' was successfully created' )
            return redirect('adminDashboard')
    context = {'form': form}
    return render(request, 'main/userRegister.html', context)

@unauthenticated
def studentRegister(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            id=request.POST.get('id')
            
            student=Student.objects.get(id=id)
            student.user=user
            student.save()

            messages.success(request, 'Account for '+username+ ' was successfully created' )
            return redirect('studentDashboard')
    context = {'form': form}
    return render(request, 'main/studentRegister.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def test(request):
    stud_class = StudentClass.objects.get(id=2)
    print(stud_class.name, ' ', stud_class.class_teacher)
    print(stud_class.students.all())

    geo_students = stud_class.studentinclass_set.all()
    for student in geo_students:
        print(student)

    level = ClassLevel.objects.get(id=1)
    form1_students = level.student_set.all()
    for student in form1_students:
        print(student.first_name)

    student=Student.objects.get(id=1)

    subjects = student.subject_set.all()
    print(subjects, '----------')

    teacher=Teacher.objects.get(id=3)
    for subject in teacher.subject_set.all():
        print(subject)

    student = Student.objects.get(id=3)
    subject = Subject.objects.get(id=4)
    
    subject.students.add(student)

    context={'subjects': subjects,'form1_students':form1_students, 'geo_students':geo_students, 'stud_class':stud_class}
    return render(request, 'dashboard/principalDashboard/test.html', context)