import time
import warnings
from calendar import month_name
from taggit.models import Tag

from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.template.loader import Context, get_template
from django.template.response import TemplateResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator, \
    InvalidPage, EmptyPage
from django.shortcuts import render, render_to_response, \
    HttpResponseRedirect, HttpResponse, get_object_or_404, redirect

from .models import Post, Comment
from .forms import CommentsForm, CommentForm, RegistrationForm, \
    LoginForm


def post(request, post_id):
    """Single post with comments and a comment form."""

    try:
        tags = Tag.objects.all()
        post_model = Post.objects.get(pk=post_id)
        comment_model = Comment.objects.filter(post=post_model)
        d = {'post': post_model, 'comments': comment_model,
             'form': CommentForm(), 'user': request.user,
             'months': mkmonth_lst(),
             'post_two': Post.objects.all(),
             'tags': tags}
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
    for y in range(year, fyear - 1, -1):
        start, end = 12, 0
        if y == year:
            start = month
        if y == fyear:
            end = fmonth - 1

        for m in range(start, end, -1):
            months.append((y, m, month_name[m]))
    return months


def month(request, year, month):
    """Monthly archive."""
    posts = Post.objects.filter(created__year=year,
                                created__month=month)
    tags = Tag.objects.all()
    return render(request, "archive.html", {'posts': posts, 'post_list': posts,
                  'months': mkmonth_lst(),
                  'post_two': Post.objects.all(),
                  'tags': tags,
                  'archive': True})


def year(request, year):
    """Yearly Archive"""
    posts = Post.objects.filter(created__year=year)
    tags = Tag.objects.all()
    return render(request, "archive.html", {'posts': posts,
                                            'post_list': posts,
                                            'months': mkmonth_lst(),
                                            'post_two': Post.objects.all(),
                                            'tags': tags,
                                            'archive': True})


def date(request, year, month, date):
    """Yearly Archive"""
    posts = Post.objects.filter(created__year=year,
                                created__month=month,
                                created__date=date)
    tags = Tag.objects.all()
    return render(request, "archive.html", {'posts': posts,
                                            'post_list': posts,
                                            'months': mkmonth_lst(),
                                            'post_two': Post.objects.all(),
                                            'tags': tags,
                                            'archive': True})


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
    tags = Tag.objects.all()
    entries_per_page = getattr(settings, 'BLOG_NUMBER_OF_ENTRIES_PER_PAGE')
    paginator = Paginator(posts, entries_per_page)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render(request, "list.html", {'posts': posts,
                                         'post_two': Post.objects.all(),
                                         'post_list': posts.object_list,
                                         'tags': tags,
                                         'months': mkmonth_lst()})


def recentposts(request):
    try:
        posts = Post.objects.all()
        comments = Comment.objects.all()
        tags = Tag.objects.all()
        comment_form = CommentsForm()
        return render(request, 'recentposts.html',
                      {'posts': posts,
                       'comments': comments,
                       'comment_form': comment_form,
                       'tags': tags,
                       'months': mkmonth_lst()})
    except Post.DoesNotExist:
        raise Http404


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration/LoginForm.html',
        variables,
    )


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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
    messages.success(request, "You Have Successfully Logged Out")
    return redirect(reverse("main"), args=[])


class AboutMe(TemplateView):
    template_name = "aboutme.html"


def tag_details(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    tags = Tag.objects.all()
    # tagged_entries = Post.objects.filter(tags__in=[tag])
    d = {'posts': posts, 'tag': tag, 'months': mkmonth_lst(),
         'post_two': Post.objects.all(), 'tags': tags}
    return render(request, "tag_details.html", d)


def authorposts(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.post_set.all()
    tags = Tag.objects.all()
    return render(request, "author.html", {'posts': posts, 'post_list': posts,
                                           'author': author,
                                           'months': mkmonth_lst(),
                                           'tags': tags,
                                           'post_two': Post.objects.all()})


def forgot_password(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        # send_mail("password reset", subject, from_email, to)
        request.POST.get('email')
    else:
        request.POSt.get('email')
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
