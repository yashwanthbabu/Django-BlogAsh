from django.contrib import admin
from django.conf.urls import patterns, include, url
from blog.views import AboutMe
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^blog/', 'blog.views.blog', name='main'),
    url(r"post/(?P<post_id>[0-9]+)/$", 'blog.views.post', name='post'),
    url(r"^add_comment/(?P<post_id>[0-9]+)/$", 'blog.views.add_comment', name='add_comment'),
    url(r"^month/(?P<year>\d{4})/(?P<month>(0|1)?\d)/$", 'blog.views.month', name='month'),
    url(r"^delete_comment/(?P<post_pk>[0-9]+)/$", 'blog.views.delete_comment', name='delete_comment'),
    url(r"^delete_comment/(?P<post_pk>[0-9]+)/(?P<comment_id>[0-9]+)/$", 'blog.views.delete_comment', name='delete_comment'),
    url(r"^aboutme/", AboutMe.as_view(), name='aboutme'),
    url(r"^posts/", 'blog.views.posts', name='recentposts'),
    # url(r'^$', 'sampleblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
