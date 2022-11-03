from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from datetime import datetime
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from task.forms import AddTaskForm, DetailTaskForm, TaskCommentForm, TaskUserLoginForm, TaskUserRegisterForm, ImgToForm, \
    DocumentToForm
from task.models import Task


class IntebUserRegisterView(CreateView):
    form_class = TaskUserRegisterForm
    template_name = 'task/add_user.html'

    def get_success_url(self):
        return reverse_lazy('task:tasks')


class TaskUserLoginView(LoginView):
    template_name = 'task/login.html'
    form_class = TaskUserLoginForm

    def get_success_url(self):
        return reverse_lazy('task:tasks')


@login_required
def tasks(request):
    title = 'Задачи'
    all_tasks = Task.objects.all().order_by('-id')
    search_query = request.GET.get('query')
    if not search_query:
        search_query = ''

    if search_query != '':
        all_tasks = Task.objects.filter(theme__contains=search_query)
    paginator = Paginator(all_tasks, 30)
    page_number = request.GET.get('page')
    task_obj = paginator.get_page(page_number)

    context = {
        'title': title,
        'task_obj': task_obj,
    }

    return render(request, 'task/tasks.html', context)


@login_required
def add_task(request):
    title = 'Новая задача'
    task_form = AddTaskForm

    if request.method == 'POST':
        task_form = AddTaskForm(request.POST, request.FILES)
        print(type(request.user))
        if task_form.is_valid:
            form = task_form.save(commit=False)
            form.author = request.user
            form.save()
            return HttpResponseRedirect(reverse('task:tasks'))

    context = {
        'title': title,
        'form': task_form,
        'user': request.user,
    }

    return render(request, 'task/add_task.html', context=context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    title = f'Задача {task.id} - {task.theme}'
    task_form = DetailTaskForm(request.POST, request.FILES, instance=task)
    img = ImgToForm(request.POST, request.FILES)
    comment = TaskCommentForm(request.POST, request.FILES)
    document = DocumentToForm(request.POST, request.FILES)

    if request.method == 'POST':
        if task_form.is_valid() and comment.is_valid() and img.is_valid() and document.is_valid():
            task_form2 = task_form.save(commit=False)
            comment_form = comment.save(commit=False)
            img_form = img.save(commit=False)
            document_form = document.save(commit=False)
            task_form2.update_author = request.user
            task_form2.save()

            if comment_form.comment != '':
                comment_form.task = Task.objects.get(id=pk)
                comment_form.author = request.user
                task_form.save()
                comment_form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif img_form.img != '':
                img_form.task_img = Task.objects.get(id=pk)
                task_form.save()
                img_form.save()

            elif document_form.document != '':
                document_form.task_doc = Task.objects.get(id=pk)
                task_form.save()
                document_form.save()

            else:
                task_form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        task_form = DetailTaskForm(instance=task)
        img = ImgToForm()
        comment = TaskCommentForm()

    context = {
        'title': title,
        'update_form': task_form,
        'task': task,
        'img': img,
        'doc': document,
        'comment': comment,

    }

    return render(request, 'task/task_detail.html', context=context)
