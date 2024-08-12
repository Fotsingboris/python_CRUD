from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.db import transaction
from .models import Student

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
