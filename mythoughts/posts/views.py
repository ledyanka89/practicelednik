from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from posts.models import Posts, PostLike
from blog.models import Blogs

from users.models import Users

from users.views import is_admin

from posts.forms import PostForm

from posts.forms import CommentForm


def posts_list(request):
    query = request.GET.get('q')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')

    if order == 'asc':
        sort_by = sort_by
    else:
        sort_by = f'-{sort_by}'

    posts = Posts.objects.order_by(sort_by)

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(author__username__icontains(query))
        ).distinct()

    if date_from:
        date_from_parsed = parse_date(date_from)
        if date_from_parsed:
            posts = posts.filter(created_at__gte=date_from_parsed)

    if date_to:
        date_to_parsed = parse_date(date_to)
        if date_to_parsed:
            posts = posts.filter(created_at__lte=date_to_parsed)

    context = {
        'posts': posts,
        'query': query,
        'date_from': date_from,
        'date_to': date_to,
        'sort_by': sort_by,
        'order': order,
    }
    return render(request, 'posts.html', context)

@login_required
def my_posts(request):
    user = request.user
    custom_user = get_object_or_404(Users, username=user.username)
    posts = Posts.objects.filter(author=custom_user).order_by('-created_at')
    owned_blogs = Blogs.objects.filter(owner=custom_user)
    authored_blogs = Blogs.objects.filter(authors=custom_user).exclude(owner=custom_user)

    if request.method == 'POST' and 'add_author' in request.POST:
        blog_id = request.POST.get('blog_id')
        username = request.POST.get('username')
        try:
            new_author = Users.objects.get(username=username)
            blog = Blogs.objects.get(id=blog_id)
            if blog.owner == custom_user:
                blog.authors.add(new_author)
                blog.save()
                print(f"Author {username} added to blog {blog.title}")
                print(f"Current authors: {[author.username for author in blog.authors.all()]}")
        except Users.DoesNotExist:
            pass

    context = {
        'posts': posts,
        'owned_blogs': owned_blogs,
        'authored_blogs': authored_blogs,
    }
    return render(request, 'myposts.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog')
        blog = get_object_or_404(Blogs, id=blog_id)
        title = request.POST.get('title')
        body = request.POST.get('body')
        custom_user = get_object_or_404(Users, username=request.user.username)
        post = Posts.objects.create(
            author=custom_user,
            blog=blog,
            title=title,
            body=body,
            created_at=timezone.now(),
            is_published=True
        )
        return redirect('post:my_posts')
    return redirect('post:my_posts')

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        custom_user = get_object_or_404(Users, username=request.user.username)
        blog = Blogs.objects.create(
            title=title,
            description=description,
            owner=custom_user
        )
        blog.authors.add(custom_user)
        return redirect('post:my_posts')
    return redirect('post:my_posts')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    user = get_object_or_404(Users, username=request.user.username)

    if PostLike.objects.filter(user=user, post=post).exists():
        return JsonResponse({'message': 'You have already liked this post.'}, status=400)

    PostLike.objects.create(user=user, post=post)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes})

@login_required
def view_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    post.views += 1
    post.save()
    return JsonResponse({'views': post.views})

@login_required
def edit_post(request, post_id):
    if not is_admin(request):
        return HttpResponseForbidden()
    post = get_object_or_404(Posts, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:blog_detail', blog_id=post.blog.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    if not is_admin(request):
        return HttpResponseForbidden()
    post = get_object_or_404(Posts, id=post_id)
    post.delete()
    return redirect('blog:blog_detail', blog_id=post.blog.id)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    custom_user = get_object_or_404(Users, username=request.user.username)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = custom_user
            comment.save()
            return redirect('post:post_detail', post_id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'user': custom_user,
        'form': form,
    }
    return render(request, 'post_detail.html', context)