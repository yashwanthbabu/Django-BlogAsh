from django.contrib import admin
from .models import Post, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    display_fields = ["title", "created"]
<<<<<<< HEAD
=======

>>>>>>> 204c2f945a754c8687159235ca4071e777ea0ebb

class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "author", "created"]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
<<<<<<< HEAD

=======
>>>>>>> 204c2f945a754c8687159235ca4071e777ea0ebb
