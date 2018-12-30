from django.db import models
from django.contrib.auth.models import User
import PIL
from PIL import Image
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill
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

    def query_messages(self):
        return self.messages.all().order_by('-pub_date')

    def query_messages_with_counter(self, counter):
        return Message.objects.filter(chat=self, id__lt=counter).order_by('-pub_date')

    def query_newer_messages(self, newest):
        return Message.objects.filter(chat=self, id__gt=newest)

    def count_new_messages(self, user):
        counter = 0
        for message in self.messages.all().filter(is_read = False):
            if message.is_grey_for_me(user):
                counter =counter + 1
        return counter

    def companions(self, user):
        companions = self.members.all()
        Companions = companions.exclude(id = user.id)
        return Companions

class Message(models.Model):
    writer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'his_written_messages', verbose_name='Автор сообщения')
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE, related_name = 'messages', verbose_name='Чат, к которому относится сообщение' )
    text = models.CharField(max_length=1000, verbose_name='Текст сообщения')
    pub_date = models.DateTimeField("Дата отправки", auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name='Прочитано ли сообщение')
    who_read = models.ManyToManyField(User, related_name = 'read_messages', verbose_name='Кто прочел сообщение')

    class Meta:
        ordering=['pub_date']
        get_latest_by = 'pub_date'
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


    def is_grey(self, user):
        if self.is_read:
            return False
        else:
            if self.chat.is_group:
                if user in self.who_read.all() and self.who_read.all().count()>=2:
                    return False
                else:
                    return True
            else:
                return True

    def is_grey_for_me(self, user):
        if user not in self.who_read.all():
            return True
        else:
            return False

    def checking_on_read(self):
        if self.who_read.all().count() == self.chat.members.all().count():
            self.is_read = True
            self.save()
            return

    def images_urls(self):
        images_urls = []
        images = ImageMessage.objects.filter(message = self)
        if images.exists():
            for image in images:
                images_urls.append({'small': '/static'+str(image.image_ultra.url), 'big': '/static'+str(image.image.url)})
            return images_urls
        else:
            return None

class ImageMessage(models.Model):
    message = models.ForeignKey(Message, on_delete = models.CASCADE, verbose_name="Сообщение", related_name = 'images')
    image = models.ImageField(upload_to="messages_images/")
    image_small = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(100, 100)], format = 'JPEG', options = {'quality' : 75})
    image_ultra = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(50, 50)], format = 'JPEG', options = {'quality' : 50})

    class Meta:
        verbose_name = "Картинка сообщения"
        verbose_name_plural = "Картинки сообщений"

    def __str__(self):
        return self.message.writer.username
