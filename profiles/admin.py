from django.contrib import admin
from profiles.models import Profile, Post, Like, Following, ImagePost, Comment, ImageComment
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user')

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('liker', 'post')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentator', 'post', 'answer_to', 'com_date')

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Following)
admin.site.register(ImagePost)
admin.site.register(Comment)
admin.site.register(ImageComment)
