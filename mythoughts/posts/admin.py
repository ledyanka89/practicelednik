from django.contrib import admin

from posts.models import Posts

from posts.models import Comments

# Register your models here.
admin.site.register(Posts)
admin.site.register(Comments)