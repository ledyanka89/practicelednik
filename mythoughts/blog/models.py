from django.db import models

from users.models import Users


class Blogs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(Users, related_name='authored_blogs',blank=True)
    owner = models.ForeignKey(Users, related_name='owned_blogs', on_delete=models.CASCADE)
    class Meta:
        db_table = "blog"
        verbose_name="Блог"
        verbose_name_plural = "Блоги"
    def __str__(self):
        return self.title
class Subscription(models.Model):
    user = models.ForeignKey(Users, related_name='subscriptions', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, related_name='subscribers', on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')
        db_table = "subscription"
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f'{self.user} подписан на {self.blog}'