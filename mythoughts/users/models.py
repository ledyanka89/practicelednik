from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=150, unique=True)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=50, verbose_name="Пароль",default="NULL")
    class Meta:
        db_table = "user"
        verbose_name="Пользователь"
        verbose_name_plural = "Пользователи"
    def __str__(self):
        return self.username
