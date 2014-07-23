from django.shortcuts import render, render_to_response, HttpResponseRedirect, redirect

# Create your views here.

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf

from .models import Post, Comment
from django.forms import ModelForm

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]





def post(request, post_id):
    """Single post with comments and a comment form."""
    
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
    d.update(csrf(request))
    print request
    return render_to_response("post.html", d)

def add_comment(request, post_id):
    """Add a new comment."""
    p = request.POST

    if p.has_key("body") and p["body"]:
        author = "Anonymous"
        if p["author"]: author = p["author"]

        comment = Comment(post=Post.objects.get(pk=post_id))
        cf = CommentForm(p, instance=comment)
        cf.fields["author"].required = False

        comment = cf.save(commit=False)
        comment.author = author
        comment.save()
    return redirect("main")

def blog(request):
    """Main listing."""
    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 3)

    try: 
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response("list.html", dict(posts=posts, user=request.user))

