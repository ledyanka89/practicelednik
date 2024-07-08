from django.urls import path

from users.views import login_view, registration_view, logout_view, delete_user, user_list

app_name = 'users'
urlpatterns = [
    path('avtorisation/', login_view,name='login'),
    path('registration/', registration_view, name='registration'),
    path('logout/', logout_view, name='logout'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('user-list/', user_list, name='user_list'),
]