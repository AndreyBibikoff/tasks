from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from task.models import Task, TaskComment, TaskUser, Images, Documents
from tasks import settings


class TaskUserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = TaskUser
        fields = ['username', 'password1', 'password2']


class TaskUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control form-outline form-label mb-4'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-outline form-label mb-4'}))


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['theme', 'deadline', 'text', 'executor']

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.fields['deadline'].widget = widgets.AdminDateWidget()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DetailTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'theme', 'deadline', 'text', 'executor']

    def __init__(self, *args, **kwargs):
        super(DetailTaskForm, self).__init__(*args, **kwargs)
        self.fields['deadline'].widget = widgets.AdminDateWidget()
        for field_name, field in self.fields.items():
            if field_name != 'author':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['disabled'] = True


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(TaskCommentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['cols'] = '110'
            field.widget.attrs['rows'] = '6'


class ImgToForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['img']


class DocumentToForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['document']
