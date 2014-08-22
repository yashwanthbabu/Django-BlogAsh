from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from blog.views import AboutMe

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^blog/', 'blog.views.blog', name='main'),
    url(r"post/(?P<post_id>[0-9]+)/$", 'blog.views.post', name='post'),
    url(r"^add_comments/", 'blog.views.add_comment', name='add_comments'),
    url(r"^add_comment/(?P<post_id>[0-9]+)/$", 'blog.views.add_comment', name='add_comment'),
    url(r"^month/(?P<year>\d{4})/(?P<month>(0|1)?\d)/$", 'blog.views.month', name='month'),
    url(r"^delete_bulk_comment/(?P<post_pk>[0-9]+)/$", 'blog.views.delete_bulk_comment', name='delete_comment'),
    url(r"^delete_single_comment/(?P<post_pk>[0-9]+)/(?P<comment_pk>[0-9]+)/$", 'blog.views.delete_single_comment', name='delete_single_comment'),
    # url(r"^aboutme/", AboutMe.as_view(), name='aboutme'),
    url(r"^recentposts/", 'blog.views.recentposts', name='recentposts'),
    #url(r"^accounts/profile", 'blog.views.blog', name='main'),
    url(r"^users/login/$", TemplateView.as_view(template_name="registrationform.html"), name='login'),
    url(r"^tag/(?P<tag_slug>[-\w]+)/$", 'blog.views.tag_details', name='tag_details'),
    url(r'^author/(?P<username>[\w.@+-]+)/$', 'blog.views.authorposts', name='author'),
    url(r'', include('social_auth.urls')),
    url(r"^logout/", 'blog.views.logout', name='logout'),
    # url(r'^$', 'sampleblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^django-session-idle-timeout/', include('django-session-idle-timeout.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
