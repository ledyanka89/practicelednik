from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from users.forms import LoginForm

from users.models import Users

from users.forms import AdministratorsRegistrationForm, UserRegistrationForm


# Create your views here.
def is_admin(request):
    return request.session.get('user_type') == 'admin'
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Проверка администратора
            try:
                user = Users.objects.get(username=username)
                if user.password == password:
                    # Аутентификация пользователя в системе Django
                    django_user = authenticate(request, username=username, password=password)
                    if django_user is None:
                        # Создание Django пользователя, если его нет
                        from django.contrib.auth.models import User
                        django_user = User.objects.create_user(username=username, password=password)
                        django_user.save()
                        django_user = authenticate(request, username=username, password=password)

                    if django_user:
                        login(request, django_user)
                        request.session['username'] = user.username
                        if user.is_admin:
                            request.session['user_type'] = 'admin'
                        else:
                            request.session['user_type'] = 'user'
                        return redirect('main:index')
            except Users.DoesNotExist:
                pass
    else:
        form = LoginForm()
    return render(request, 'avtorisation.html', {'form': form})

def registration_view(request):
    # Инициализация форм для GET-запроса
    admin_form = AdministratorsRegistrationForm()
    user_form = UserRegistrationForm()

    if request.method == 'POST':
        if 'admin' in request.POST:
            admin_form = AdministratorsRegistrationForm(request.POST)
            if admin_form.is_valid():
                code_word = admin_form.cleaned_data['code_word']
                if code_word == '8642':
                    admin_instance = admin_form.save(commit=False)
                    admin_instance.is_admin = True
                    admin_instance.save()
                    return redirect('main:index')
                else:
                    admin_form.add_error('code_word', 'Неверное кодовое слово')
        elif 'user' in request.POST:
            print("cola")
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                user_instance = user_form.save(commit=False)
                user_instance.is_admin = False
                user_instance.save()
                return redirect('main:index')

    return render(request, 'registration.html', {'admin_form': admin_form, 'client_form': user_form})

def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    logout(request)
    return redirect('main:index')

from django.contrib.auth.decorators import login_required

@login_required
def user_list(request):
    if not is_admin(request):
        return HttpResponseForbidden()
    users = Users.objects.filter(is_admin=False)
    context = {
        'users': users
    }
    return render(request, 'user_list.html', context)



@login_required
def delete_user(request, user_id):
    if not is_admin(request):
        return HttpResponseForbidden()
    user = get_object_or_404(Users, id=user_id)
    if user.is_admin:
        return HttpResponseForbidden()  # Нельзя удалять администраторов
    user.delete()
    return redirect('users:user_list')