from django.db import models
from django.utils import timezone

from blog.models import Blogs
from users.models import Users


class Posts(models.Model):
    author = models.ForeignKey(Users, related_name='posts', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.is_published and not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comments(models.Model):
    author = models.ForeignKey(Users, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class PostLike(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')