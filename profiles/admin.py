from django.contrib import admin
from profiles.models import Profile, Post, Like
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user')


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('liker', 'post')

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
