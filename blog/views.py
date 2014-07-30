import time
import pytz
from calendar import month_name
from django.conf import settings
from django.shortcuts import render, \
    render_to_response, HttpResponseRedirect, redirect
from django.http import Http404
from django.template import RequestContext
import time
from calendar import month_name
from django.core.mail import send_mail
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from .models import Post, Comment
from .forms import ModelForm
from .forms import CommentForm


def post(request, post_id):
    """Single post with comments and a comment form."""
    try:
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post)
        d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
        d.update(csrf(request))
        print request
        return render_to_response("post.html", d)
    except Post.DoesNotExist:
        raise Http404


def add_comment(request, post_id):
    """Add a new comment."""
    p = request.POST

    if p.has_key("body") and p["body"]:
        author = "Anonymous"
        if p["author"]:
            author = p["author"]

        comment = Comment(post=Post.objects.get(pk=post_id))
        cf = CommentForm(p, instance=comment)
        cf.fields["author"].required = False

        comment = cf.save(commit=False)
        comment.author = author
	comment.save()
    return redirect("main")


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
    return render_to_response("archive.html", dict(posts=posts, post_list=posts,
                                     context_instance=RequestContext(request),
                                                months=mkmonth_lst(), archive=True))


def delete_comment(request, post_pk, pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        if not pk: pklst = request.POST.getlist("delete")
        else: pklst = [pk]
	print request
        for pk in pklst:
            Comment.objects.get(pk=pk).delete()
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

    return render_to_response("list.html", dict(posts=posts,
                                                context_instance=RequestContext(request),
                                                post_list=posts.object_list, months=mkmonth_lst()))


def aboutme(request):
    return render_to_response("aboutme.html")
