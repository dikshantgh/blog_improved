from django.contrib import admin

# Register your models here.
from blog.models import CustomUser, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display =('title', 'author',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('age', 'username', 'email',)


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
