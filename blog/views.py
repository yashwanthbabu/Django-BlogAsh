import time
from calendar import month_name

from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import Context, get_template
from django.core.paginator import Paginator, \
    InvalidPage, EmptyPage
from django.shortcuts import render, \
    HttpResponseRedirect, HttpResponse

from .models import Post, Comment
from .forms import CommentsForm, CommentForm


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
            'author': request.POST.get("author"),
            'body': request.POST.get("body")}))
        if form.is_valid():
            comment_author = "Anonymous"
            if request.POST["author"]:
                comment_author = request.POST["author"]

            comment = Comment(post=Post.objects.get(pk=post_id))
            cf = CommentForm(request.POST, instance=comment)
            cf.fields["author"].required = False

            comment = cf.save(commit=False)
            comment.author = comment_author
            comment.save()
            form = CommentForm()

            try:
                send_mail("Comment added", subject, from_email, to)
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
    posts = Post.objects.filter(created__year=year, created__month=month)
    return render(request, "archive.html", {'posts': posts, 'post_list': posts,
                  'months': mkmonth_lst(), 'archive': True})


def delete_bulk_comment(request, post_pk, pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        import ipdb
        ipdb.set_trace()
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
    posts = Post.objects.order_by("-created")
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
                  'post_list': posts.object_list, 'months': mkmonth_lst()})


def posts(request):
    try:
        posts = Post.objects.order_by("-created")
        comments = Comment.objects.order_by("created")
        comment_form = CommentsForm()
        return render(request, 'recentposts.html', {'posts': posts,
                      'comments': comments, 'comment_form': comment_form,
                      'months': mkmonth_lst()})
    except Post.DoesNotExist:
        raise Http404


class AboutMe(TemplateView):
    template_name = "aboutme.html"
