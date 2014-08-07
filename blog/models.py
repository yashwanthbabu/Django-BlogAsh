from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=60)
    user = models.ForeignKey(User, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=60)
    email = models.EmailField(max_length=35, null=True)
    body = models.TextField()
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))
