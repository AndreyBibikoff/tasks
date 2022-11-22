"""tasks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from task.views import tasks, add_task, task_detail, TaskUserLoginView, IntebUserRegisterView

app_name = 'task'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_user/', IntebUserRegisterView.as_view(), name='add_user'),
    path('', TaskUserLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('tasks/', tasks, name='tasks'),
    path('add_task/', add_task, name='add_task'),
    path('task_detail/<int:pk>/', task_detail, name='task_detail'),
    path("logout/", LogoutView.as_view(), name="logout"),

]
