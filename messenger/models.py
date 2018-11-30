from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    members = models.ManyToManyField(User, verbose_name='Участник чата', related_name='chats')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название чата')
    create_data = models.DateField("Дата создания", auto_now_add=True)
    is_group = models.BooleanField()

    class Meta:
        ordering = ['create_data']
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

class Message(models.Model):
    writer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'his_written_messages', verbose_name='Автор сообщения')
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE, related_name = 'messages', verbose_name='Чат, к которому относится сообщение' )
    text = models.CharField(max_length=1000, verbose_name='Текст сообщения')
    pub_date = models.DateTimeField("Дата отправки", auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name='Прочитано ли сообщение')
    who_read = models.ManyToManyField(User, related_name = 'read_messages', verbose_name='Кто прочел сообщение')

    class Meta:
        ordering=['-pub_date']
        get_latest_by = 'pub_date'
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
