import time
from calendar import month_name

from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout as auth_logout
from django.core.context_processors import csrf
from taggit.models import Tag
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import Context, get_template
from django.core.paginator import Paginator, \
    InvalidPage, EmptyPage
from django.shortcuts import render, \
    HttpResponseRedirect, HttpResponse, get_object_or_404, redirect

from .models import Post, Comment
from .forms import CommentsForm, CommentForm, MyRegistrationForm, \
    LoginForm

import warnings
from django.template.response import TemplateResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator


@login_required
def home(request):
    return HttpResponse('Home Page')


def post(request, post_id):
    """Single post with comments and a comment form."""

    try:
        post_model = Post.objects.get(pk=post_id)
        comment_model = Comment.objects.filter(post=post_model)
        d = {'post': post_model, 'comments': comment_model,
             'form': CommentForm(), 'user': request.user,
             'months': mkmonth_lst()}
        return render(request, "post.html", d,)
    except Post.DoesNotExist:
        raise Http404


def add_comment(request, post_id):

    form = CommentForm(request.POST)
    post_model = Post.objects.get(pk=post_id)
    comment_model = Comment.objects.filter(post=post_model)
    from_email = ""
    mail = request.POST.get("email")
    to = [mail]
    if request.method == 'POST':
        form = CommentForm(request.POST)
        subject = get_template('blog/mail.txt').render(Context({
            'author': request.POST.get("name"),
            'body': request.POST.get("body")}))
        if form.is_valid():
            comment_author = "Anonymous"
            if request.POST["name"]:
                comment_author = request.POST["name"]

            comment = Comment(post=Post.objects.get(pk=post_id))
            cf = CommentForm(request.POST, instance=comment)
            cf.fields["name"].required = False

            comment = cf.save(commit=False)
            comment.author = comment_author
            comment.save()
            form = CommentForm()

            try:
                send_mail("Comment added", subject, from_email, to)
                form = CommentForm()
                return HttpResponseRedirect('#comment-%s' % comment.pk)
            except BadHeaderError:
                return HttpResponse("invalid header error")
    else:
        form = CommentsForm()
    d = {'post': post_model, 'comments': comment_model,
         'form': form, 'months': mkmonth_lst()}
    return render(request, "post.html", d)


def mkmonth_lst():
    """Make a list of months to show archive links."""
    if not Post.objects.count():
        return []

    # set up vars
    year, month = time.localtime()[:2]
    first = Post.objects.earliest("created")
    fyear = first.created.year
    fmonth = first.created.month
    months = []

    # loop over years and months
    for y in range(year, fyear-1, -1):
        start, end = 12, 0
        if y == year:
            start = month
        if y == fyear:
            end = fmonth-1

        for m in range(start, end, -1):
            months.append((y, m, month_name[m]))
    return months


def month(request, year, month):
    """Monthly archive."""
    if request.user.is_authenticated():
        messages.success(request, "you are successfully logged in")
    posts = Post.objects.filter(created__year=year,
                                created__month=month)
    return render(request, "archive.html", {'posts': posts, 'post_list': posts,
                  'months': mkmonth_lst(), 'archive': True})


def delete_bulk_comment(request, post_pk, pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        if not pk:
            pklst = request.POST.getlist("delete")
        else:
            pklst = [pk]
        for pk in pklst:
            Comment.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse("post", args=[post_pk]))


def delete_single_comment(request, post_pk, comment_pk, pk=None):
    obj = Comment.objects.get(pk=comment_pk)
    obj.delete()
    return HttpResponseRedirect(reverse("post", args=[post_pk]))


def blog(request):
    """Main listing."""
    posts = Post.objects.all()
    entries_per_page = getattr(settings, 'BLOG_NUMBER_OF_ENTRIES_PER_PAGE')
    paginator = Paginator(posts, entries_per_page)
    if request.user.is_authenticated():
        messages.success(request, "you are successfully logged in")
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render(request, "list.html", {'posts': posts,
                  'post_list': posts.object_list, 'months': mkmonth_lst()})


def recentposts(request):
    if request.user.is_authenticated():
        messages.success(request, "you are successfully logged in")
    try:
        posts = Post.objects.all()
        comments = Comment.objects.all()
        comment_form = CommentsForm()
        return render(request, 'recentposts.html',
                      {'posts': posts,
                       'comments': comments, 'comment_form': comment_form,
                       'months': mkmonth_lst()})
    except Post.DoesNotExist:
        raise Http404


def register_user(request):
    if request.method == "POST":
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('main')
    args = {}
    args.update(csrf(request))

    args['form'] = MyRegistrationForm()

    return render(request, "register.html", args)


def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username
        print password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                state = "Your account is not active, Contact Admin."
        else:
            messages.success(request, "Your Username/Password were incorrect")
            return render(request, "registration/login.html")

    return redirect(reverse('main'), args={'state': state,
                                           'username': username,
                                           'password': password})


def logout(request):
    """Logs out user"""
    auth_logout(request)
    messages.success(request, "you have successfully logged out")
    return redirect(reverse("main"), args=[])


class AboutMe(TemplateView):
    template_name = "aboutme.html"


def tag_details(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    # tagged_entries = Post.objects.filter(tags__in=[tag])
    d = {'posts': posts, 'tag': tag}
    return render(request, "tag_details.html", d)


def authorposts(request, username):
    author = get_object_or_404(User, username=username)
    print author
    posts = author.post_set.all()
    return render(request, "author.html", {'posts': posts, 'post_list': posts,
                                           'author': author,
                                           'months': mkmonth_lst()})


def forgot_password(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        # send_mail("password reset", subject, from_email, to)
        from_email = request.POST.get('email')
        print from_email
    else:
        from_email = request.POSt.get('email')
        print from_email
        return render(request, 'registration/password_reset_form.html')


def reset_confirm(request, uidb64=None, token=None):
    # Wrap the built-in reset confirmation view and
    # pass to it all the captured parameters like uidb64, token
    # and template name, url to redirect after password reset is confirmed.
    return password_reset_confirm(request, template_name='reset_confirm.html',
                                  uidb64=uidb64, token=token,
                                  post_reset_redirect=reverse('success'))


def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {'use_https': request.is_secure(),
                    'token_generator': token_generator,
                    'from_email': from_email,
                    'request': request,
                    'html_email_template_name': html_email_template_name,
                    }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 2.0.",
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {'form': form, 'title': _('Password reset'), }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_confirm(request, uidb64=None, token=None,
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert [uidb64 is not None, token is not None]  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
        context = {'form': form, 'title': title, 'validlink': validlink, }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, context,
                            current_app=current_app)
