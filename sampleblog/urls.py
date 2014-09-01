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
    url(r"^recentposts/", 'blog.views.recentposts', name='recentposts'),
    url(r"^users/register/$", TemplateView.as_view(template_name="LoginForm.html"), name='loginform'),
    url(r"^tag/(?P<tag_slug>[-\w]+)/$", 'blog.views.tag_details', name='tag_details'),
    url(r'^users/(?P<username>[\w.@+-]+)/$', 'blog.views.authorposts', name='author'),
    url(r'', include('social_auth.urls')),
    url(r'^login/', 'blog.views.login_user', name='loginuser'),
    url(r'^accounts/register/$', 'blog.views.register', name="register"),
    url(r'^register/success/$', 'blog.views.register_success', name="register_success"),
    # url(r'^register/', 'blog.views.register_user', name='register_user'),
    url(r"^logout/", 'blog.views.logout', name='logout'),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^forgot-password/$','blog.views.password_reset', name="forgot-password"),
    url(r'^password_reset/$', 'blog.views.password_reset', name='password_reset'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'blog.views.password_reset_confirm', name='password_confirm'),
    url(r'^django-session-idle-timeout/', include('django-session-idle-timeout.urls')),
    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password/reset/done/'}, name='reset'),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'blog.views.password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password/done/'}, name='password-reset-confirm'),
    url(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete', name="password-reset-complete"),
    url(r'^admin/', include(admin.site.urls)),
)
