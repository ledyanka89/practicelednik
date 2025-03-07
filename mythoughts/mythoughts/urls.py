"""
URL configuration for mythoughts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from mythoughts.settings import DEBUG

urlpatterns = [
    path('', include('main.urls', namespace='main')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('',include('blog.urls',namespace='blog')),
    path('',include('posts.urls',namespace='post')),
]
# if DEBUG:
#     urlpatterns += [
#     path("__debug__/", include("debug_toolbar.urls")),
#     ]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]