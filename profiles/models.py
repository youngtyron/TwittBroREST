from django.db import models
from django.contrib.auth.models import User
import PIL
from PIL import Image
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, primary_key=True, related_name = 'profile')
    registrated = models.DateField("Дата регистрации", auto_now_add=True)
    avatar = models.ImageField(upload_to="images/", null = True, blank = True)
    # avatar_profile = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(100, 100)], format = 'JPEG', options = {'quality' : 75})
    # avatar_mini = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(50, 50)], format = 'JPEG', options = {'quality' : 50})
    # avatar_micro = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(25, 25)], format = 'JPEG', options = {'quality' : 25})
    rating = models.PositiveIntegerField(default = 0)

    class Meta:
        ordering = ['-rating']
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def query_news(self):
        followings = Following.objects.filter(who = self.user)
        users = []
        for f in followings:
            users.append(f.to)
        users.append(self.user)
        return Post.objects.filter(author__in=users)

    def query_news_with_counter(self, counter):
        followings = Following.objects.filter(who = self.user)
        users = []
        for f in followings:
            users.append(f.to)
        users.append(self.user)
        return Post.objects.filter(author__in=users, id__lt=counter)

class Post(models.Model):
    author = models.ForeignKey(User, verbose_name="Автор", on_delete = models.CASCADE)
    text = models.CharField(max_length = 400, null = True, blank = True, verbose_name="Текст")
    pub_date = models.DateTimeField("Дата отправки", auto_now_add=True)
    likes_quanity = models.IntegerField(default = 0)
    # repost = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = 'reposted', null = True, blank = True)
    # is_repost = models.BooleanField(default = False)
    # comments_quanity = models.IntegerField(default = 0)
    # reposts_quanity = models.IntegerField(default = 0)
    # likes = GenericRelation(Like, related_query_name='posts')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Пост пользователя"
        verbose_name_plural = "Посты пользователей"

    def like(self, user):
        Like.objects.create(post = self, liker = user)
        self.likes_quanity = self.likes_quanity + 1
        self.save()
        return

    def unlike(self, user):
        like = Like.objects.get(post = self, liker = user)
        self.likes_quanity = self.likes_quanity - 1
        self.save()
        like.delete()
        return

    def user_can_likes(self, user):
        num_likes = Like.objects.filter(post  =self, liker = user).count()
        if num_likes>0:
            return False
        else:
            return True


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="Оценивший пользователь")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name="Понравившийся пост")
    when = models.DateTimeField("Дата оценки", auto_now_add=True)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

class Following(models.Model):
    who = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="Подписавшийся пользователь", related_name = 'followings')
    to = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="Пользователь на которого подписались", related_name = 'followers')
    fol_date = models.DateTimeField("Дата подписки", auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return '%s to -> %s' % (self.who, self.to)
