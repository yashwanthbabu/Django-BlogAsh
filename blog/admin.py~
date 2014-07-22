from django.contrib import admin
from blog.models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]

admin.site.register(Post, PostAdmin)


