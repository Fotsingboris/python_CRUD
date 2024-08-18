from django.urls import path
from . import views
app_name = 'students'

urlpatterns = [
    path('', views.StudentView.as_view(), name='student_view'),
    path('send-email/', views.send_email_view, name='send_email'),

]