from django.contrib import admin
from .models import Post, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    display_fields = ["title", "created"]
<<<<<<< HEAD


class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "author", "created"]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
=======

>>>>>>> 5234395f7ae24f76e99e8922cb315a3d7adbbb93

class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "author", "created"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

