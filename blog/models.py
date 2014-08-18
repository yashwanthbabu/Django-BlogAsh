from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=60)
    author = models.ForeignKey(User, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.title
        return unicode(self.created)


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=35, null=True)
    body = models.TextField()
    post = models.ForeignKey(Post)

    class meta:
        ordering = ['-created']

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))
