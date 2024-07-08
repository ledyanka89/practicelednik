from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Blogs, Subscription
from django.utils.dateparse import parse_date
from users.models import Users
from posts.models import Posts
from django.contrib.auth.decorators import login_required

from users.views import is_admin

from blog.forms import BlogForm


def blog_list(request):
    query = request.GET.get('q')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    sort_by = request.GET.get('sort_by', 'updated_at')
    order = request.GET.get('order', 'desc')

    if order == 'asc':
        sort_by = sort_by
    else:
        sort_by = f'-{sort_by}'

    blogs = Blogs.objects.all().order_by(sort_by)

    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) | Q(authors__username__icontains=query)
        ).distinct()

    if date_from:
        date_from_parsed = parse_date(date_from)
        if date_from_parsed:
            blogs = blogs.filter(created_at__gte=date_from_parsed)

    if date_to:
        date_to_parsed = parse_date(date_to)
        if date_to_parsed:
            blogs = blogs.filter(created_at__lte=date_to_parsed)

    user = get_object_or_404(Users, username=request.user.username) if request.user.is_authenticated else None
    subscriptions = Subscription.objects.filter(user=user).values_list('blog_id', flat=True) if user else []
    context = {
        'blogs': blogs,
        'user': user,
        'subscriptions': subscriptions,
        'query': query,
        'date_from': date_from,
        'date_to': date_to,
        'sort_by': sort_by,
        'order': order,
    }
    return render(request, 'blog_list.html', context)

@login_required
def subscribe(request, blog_id):
    blog = get_object_or_404(Blogs, id=blog_id)
    user = get_object_or_404(Users, username=request.user.username)
    Subscription.objects.get_or_create(user=user, blog=blog)
    return redirect('blog:blog_list')

@login_required
def unsubscribe(request, blog_id):
    blog = get_object_or_404(Blogs, id=blog_id)
    user = get_object_or_404(Users, username=request.user.username)
    subscription = Subscription.objects.filter(user=user, blog=blog)
    if subscription.exists():
        subscription.delete()
    return redirect('blog:blog_list')

@login_required
def my_subscriptions(request):
    user = get_object_or_404(Users, username=request.user.username)
    subscriptions = Subscription.objects.filter(user=user)
    context = {
        'subscriptions': subscriptions
    }
    return render(request, 'my_subscriptions.html', context)

@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blogs, id=blog_id)
    posts = Posts.objects.filter(blog=blog).order_by('-created_at')
    user = get_object_or_404(Users, username=request.user.username)
    context = {
        'blog': blog,
        'posts': posts,
        'user': user,
        'is_admin': is_admin(request)
    }
    return render(request, 'blog_detail.html', context)

@login_required
def edit_blog(request, blog_id):
    if not is_admin(request):
        return HttpResponseForbidden()
    blog = get_object_or_404(Blogs, id=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog:blog_detail', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'edit_blog.html', {'form': form})

@login_required
def delete_blog(request, blog_id):
    if not is_admin(request):
        return HttpResponseForbidden()
    blog = get_object_or_404(Blogs, id=blog_id)
    blog.delete()
    return redirect('blog:blog_list')