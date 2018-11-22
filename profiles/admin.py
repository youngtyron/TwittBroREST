from django.contrib import admin
from profiles.models import Profile, Post
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user')


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date')

admin.site.register(Profile)
admin.site.register(Post)
