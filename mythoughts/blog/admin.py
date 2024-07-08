from django.contrib import admin

from blog.models import Blogs, Subscription

# Register your models here.
admin.site.register(Blogs)
admin.site.register(Subscription)