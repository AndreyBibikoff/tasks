import os

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class TaskUser(AbstractUser):
    create = models.DateTimeField(verbose_name='создан', auto_now_add=True)


class Task(models.Model):
    New = 'N'
    In_work = 'W'
    Complete = 'C'
    Not_comlete = 'NC'
    Close = 'CLS'
    Status_CHOICES = (
        (New, 'Новая'),
        (In_work, 'В работе'),
        (Complete, 'Завершена'),
        (Not_comlete, 'Невозможно выполнить'),
        (Close, 'Закрыта'),
    )
    date = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    author = models.ForeignKey(TaskUser, verbose_name='Автор', related_name='Автор', on_delete=models.PROTECT)
    status = models.CharField(verbose_name='Статус', max_length=3, choices=Status_CHOICES, default='N')
    theme = models.CharField(verbose_name='Тема', max_length=128)
    deadline = models.DateTimeField(verbose_name='Срок')
    text = models.TextField(verbose_name='Текст', blank=True)
    executor = models.ForeignKey(TaskUser, verbose_name='Исполнитель', related_name='Исполнитель',
                                 on_delete=models.PROTECT)
    expired = models.BooleanField(default=False)
    updated = models.DateTimeField(verbose_name='Обновлена', auto_now=True)
    update_author = models.ForeignKey(TaskUser, related_name='update_author', blank=True, null=True,
                                      on_delete=models.PROTECT)


class TaskComment(models.Model):
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    author = models.ForeignKey(TaskUser, related_name='author', on_delete=models.PROTECT)
    task = models.ForeignKey(Task, related_name='comment', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True)

    def __str__(self):
        return self.comment


def image_folder(self, filename):
    folder = self.task_img
    return "{0}/{1}".format(folder, filename)


class Images(models.Model):
    img = models.ImageField(verbose_name='изображение', upload_to=image_folder, blank=True)
    task_img = models.ForeignKey(Task, related_name='task_images', on_delete=models.CASCADE)


def document_folder(self, filename):
    folder = self.task_doc
    return "{0}/{1}".format(folder, filename)


class Documents(models.Model):
    document = models.FileField(verbose_name='Документы', upload_to=document_folder, blank=True)
    task_doc = models.ForeignKey(Task, related_name='task_documents', on_delete=models.CASCADE)

    def filename(self):
        return os.path.basename(self.document.name)