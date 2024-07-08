from django.urls import path, include

from blog.views import blog_list, subscribe, unsubscribe, my_subscriptions, blog_detail, edit_blog, delete_blog

app_name = 'blog'

urlpatterns = [
    path('blog-list/', blog_list, name='blog_list'),
    path('my-subscriptions/', my_subscriptions, name='my_subscriptions'),
    path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('subscribe/<int:blog_id>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:blog_id>/', unsubscribe, name='unsubscribe'),
    path('blogs/<int:blog_id>/edit/', edit_blog, name='edit_blog'),
    path('blogs/<int:blog_id>/delete/', delete_blog, name='delete_blog'),
]