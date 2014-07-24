from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^blog/', 'blog.views.blog', name='main'),
    url(r"post/(?P<post_id>[0-9]+)/$", 'blog.views.post', name='post'),
    url(r"^add_comment/(?P<post_id>[0-9]+)/$", 'blog.views.add_comment', name='add_comment'),
    # url(r'^$', 'sampleblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)
