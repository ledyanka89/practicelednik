from django.shortcuts import render

from posts.models import Posts
from users.models import Users


def index(request):
    posts = Posts.objects.order_by('-created_at')[:5]
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    context = {
        'posts': posts,
        'user': user,
    }
    return render(request, 'index.html', context)
