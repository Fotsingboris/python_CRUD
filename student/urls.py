from django.urls import path
from . import views
app_name = 'students'

urlpatterns = [
    path('', views.StudentView.as_view(), name='student_view'),
    path('dashbord', views.AdminView.as_view(), name='home'),
    path('send-email/', views.send_email_view, name='send_email'),
    path('login_view/', views.loginView.as_view(), name='login_view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]