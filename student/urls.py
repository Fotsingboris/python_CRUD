from django.urls import path
from . import views
app_name = 'students'

urlpatterns = [
    path('', views.StudentView.as_view(), name='student_view'),
]