from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.conf import settings
=======
from django.contrib import admin
>>>>>>> 5234395f7ae24f76e99e8922cb315a3d7adbbb93

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=60)
<<<<<<< HEAD
    user = models.ForeignKey(User, null=True)
=======

>>>>>>> 5234395f7ae24f76e99e8922cb315a3d7adbbb93
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=60)
    body = models.TextField()
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))
<<<<<<< HEAD







=======
>>>>>>> 5234395f7ae24f76e99e8922cb315a3d7adbbb93
