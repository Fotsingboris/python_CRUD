from distutils import config
from email.message import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.db import transaction
from .models import Student


from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')

            return redirect('students:home')  # Redirect to a success page or home
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('students:student_view')


class StudentView(View):
    template_name = 'student/student.html'  # Update this to your template

    def get(self, request):
        students = Student.objects.all()
        return render(request, self.template_name, {'students': students})

    def post(self, request):
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        grade = request.POST.get('grade')
        action = request.POST.get('action')
        student_id = request.POST.get('id')

        try:
            with transaction.atomic():
                if action == 'create':
                    if not Student.objects.filter(name=name, email=email).exists():
                        Student.objects.create(
                            name=name,
                            age=age,
                            email=email,
                            grade=grade
                        )
                        messages.success(request, 'Student added successfully.')
                    else:
                        messages.error(request, 'Student already exists.')

                elif action == 'update':
                    student = get_object_or_404(Student, id=student_id)
                    student.name = name
                    student.age = age
                    student.email = email
                    student.grade = grade
                    student.save()
                    messages.success(request, 'Student updated successfully.')

                elif action == 'delete':
                    student = get_object_or_404(Student, id=student_id)
                    student.delete()
                    messages.success(request, 'Student deleted successfully.')

                else:
                    messages.error(request, 'Invalid action.')

        except Exception as e:
            messages.error(request, 'Error processing the request. Please try again.')

        # return render('students:student', self.template_name,)  # Redirect to the student list or appropriate page
        return redirect('students:student_view')





def send_email_view(request):
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        try:
            email = EmailMessage(
                subject,
                message,
                'your-email@gmail.com',  # or use config('MAIL_FROM_ADDRESS')
                [recipient_email],
            )
            email.send(fail_silently=False)
            return redirect('email_sent')  # Redirect to a success page
        except Exception as e:
            messages.error(request, 'Error sending email. Please try again.')
        return redirect('students:student_view')
    
    return redirect('students:student_view')


class AdminView(View):
    template_name = 'dashboard/base.html'  # Update this to your template

    def get(self, request):
        return render(request, self.template_name)
    
class loginView(View):
    template_name = 'auth/login.html'  # Update this to your template

    def get(self, request):
        return render(request, self.template_name)
    