from django.urls import path, include

from posts.views import posts_list, my_posts, create_post, create_blog, like_post, view_post, delete_post, edit_post, post_detail

app_name = 'post'

urlpatterns = [
    path('post-list/', posts_list, name='posts_list'),
    path('my-posts/', my_posts, name='my_posts'),
    path('create-post/', create_post, name='create_post'),
    path('create-blog/', create_blog, name='create_blog'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('view/<int:post_id>/', view_post, name='view_post'),
    path('posts/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]