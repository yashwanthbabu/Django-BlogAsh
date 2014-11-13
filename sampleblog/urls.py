from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:

    # Home urls
    url(r'^$', 'blog.views.home', name='home'),
    url(r'contact/',
        TemplateView.as_view(template_name="contact/contact.html"),
        name="contact"),
    url(r'feedback/',
        'blog.views.feedback',
        name="feedback"),

    # Blog urls
    url(r'^blog/', 'blog.views.blog', name='main'),
    url(r"blogpost/(?P<post_id>[0-9]+)/$", 'blog.views.post', name='post'),
    url(r"^add_comment/(?P<post_id>[0-9]+)/$", 'blog.views.add_comment',
        name='add_comment'),
    url(r"^archives/(?P<year>\d{4})/(?P<month>(0|1)?\d)/$", 'blog.views.month',
        name='month'),
    url(r"^archives/(?P<year>\d{4})/$", 'blog.views.year', name='year'),
    # url(r"^archives/(?P<year>\d{4})/(?P<month>(0|1)?\d)/(?P<day>\d+)/$",
    #     'blog.views.date', name='date'),
    url(r"^delete_bulk_comment/(?P<post_pk>[0-9]+)/$",
        'blog.views.delete_bulk_comment', name='delete_comment'),
    url(r"^delete_single_comment/(?P<post_pk>[0-9]+)/(?P<comment_pk>[0-9]+)/$",
        'blog.views.delete_single_comment', name='delete_single_comment'),
    url(r"^blogposts/recentposts/", 'blog.views.recentposts',
        name='recentposts'),
    url(r"^blogpost/tag/(?P<tag_slug>[-\w]+)/$", 'blog.views.tag_details',
        name='tag_details'),
    url(r'^author/(?P<username>[\w.@+-]+)/$', 'blog.views.authorposts',
        name='author'),
    url(r'^checkout/purchaseform/',
        TemplateView.as_view(template_name="2checkout.html"),
        name="checkout_purchase"),
    url(r'^checkout/paymentform/',
        TemplateView.as_view(template_name="2checkout_sample.html"),
        name="checkout_payment"),

    # Login and Registration urls
    url(r'^login/', 'blog.views.login_user', name='loginuser'),
    url(r'^accounts/register/$', 'blog.views.register', name="register"),
    url(r'^register/success/$', 'blog.views.register_success',
        name="register_success"),
    url(r"^logout/", 'blog.views.logout', name='logout'),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    # django-social-auth urls
    url(r'', include('social_auth.urls')),

    # Registration password reset urls
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/forgot-password/$', 'blog.views.password_reset',
        name="forgot-password"),
    url(r'^accounts/password_reset/$', 'blog.views.password_reset',
        name='password_reset'),
    url(r'^accounts/password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'blog.views.password_reset_confirm',
        name='password_confirm'),
    url(r'^accounts/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/accounts/password/reset/done/'},
        name='reset'),
    url(r'^accounts/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'blog.views.password_reset_confirm',
        {'post_reset_redirect': '/accounts/password/done/'},
        name='password-reset-confirm'),
    url(r'^accounts/password/done/$',
        'django.contrib.auth.views.password_reset_complete',
        name="password-reset-complete"),

    # Session Timeout url
    url(r'^django-session-idle-timeout/',
        include('django-session-idle-timeout.urls')),

    # Comment App url's
    # url(r'^comments/', include('django.contrib.comments.urls')),
    # url(r'^comments/(?P<post_id>[0-9]+)/$', 'blog.views.comments_count',
    #     name="comments_count"),


    # Admin url
    url(r'^console/admin/', include(admin.site.urls)),
)
