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
    avatar_small = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(100, 100)], format = 'JPEG', options = {'quality' : 75})
    avatar_ultra = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(50, 50)], format = 'JPEG', options = {'quality' : 50})
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

    def small_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return '/static' + str(self.avatar_small.url)
        else:
            return '/static/static/images/avatar.jpeg'

    def ultra_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return '/static' + str(self.avatar_ultra.url)
        else:
            return '/static/static/images/avatar.jpeg'

class Post(models.Model):
    author = models.ForeignKey(User, verbose_name="Автор", on_delete = models.CASCADE)
    text = models.CharField(max_length = 400, null = True, blank = True, verbose_name="Текст")
    pub_date = models.DateTimeField("Дата отправки", auto_now_add=True)
    likes_quanity = models.IntegerField(default = 0)
    repost = models.ForeignKey('Post', verbose_name="Репост", on_delete = models.SET_NULL, related_name = 'reposts', null = True, blank = True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Пост пользователя"
        verbose_name_plural = "Посты пользователей"

    def is_commented(self):
        comments = self.comments_to_this_post.all()
        if comments.exists():
            return True
        else:
            return False

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

    def images_urls(self):
        images_urls = []
        images = ImagePost.objects.filter(post = self)
        if images.exists():
            for image in images:
                images_urls.append({'small': '/static'+str(image.image_ultra.url), 'big': '/static'+str(image.image.url)})
            return images_urls
        else:
            return None

    def can_repost(self, user):
        if self.repost:
            if self.repost.author == user or self.author ==user:
                return False
            else:
                return True
        else:
            if self.author == user:
                return False
            else:
                return True


class ImagePost(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name="Пост", related_name = 'images')
    image = models.ImageField(upload_to="post_images/")
    image_small = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(100, 100)], format = 'JPEG', options = {'quality' : 75})
    image_ultra = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(50, 50)], format = 'JPEG', options = {'quality' : 50})

    class Meta:
        verbose_name = "Картинка поста"
        verbose_name_plural = "Картинки постов"

    def __str__(self):
        return self.post.author.username


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

class Comment(models.Model):
    commentator = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="Комментатор", related_name = 'users_comments')
    text = models.CharField(max_length = 500, null = True, blank = True, verbose_name="Текст")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name="Прокомментированный пост", related_name='comments_to_this_post')
    com_date = models.DateTimeField("Дата отправки комментария", auto_now_add=True)

    class Meta:
        ordering = ['com_date']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.commentator.username

    def images_urls(self):
        images_urls = []
        images = ImageComment.objects.filter(comment = self)
        if images.exists():
            for image in images:
                images_urls.append({'small': '/static'+str(image.image_ultra.url), 'big': '/static'+str(image.image.url)})
            return images_urls
        else:
            return None

class ImageComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, verbose_name="Коммент", related_name = 'images')
    image = models.ImageField(upload_to="comment_images/")
    image_small = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(100, 100)], format = 'JPEG', options = {'quality' : 75})
    image_ultra = ImageSpecField([Adjust(contrast = 1, sharpness = 1), ResizeToFill(50, 50)], format = 'JPEG', options = {'quality' : 50})

    class Meta:
        verbose_name = "Картинка комментария"
        verbose_name_plural = "Картинки комментариев"

    def __str__(self):
        return self.comment.commentator.username
