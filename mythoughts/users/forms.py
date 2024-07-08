from django import forms

from users.models import Users


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
class RegistrationChoiceForm(forms.Form):
    CHOICES = [('user', 'Пользователь'), ('admin', 'Администратор'), ('login', "Уже есть аккаунт")]
    registration_choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'password']
class AdministratorsRegistrationForm(forms.ModelForm):
    code_word = forms.CharField(label='Кодовое слово', max_length=10)

    class Meta:
        model = Users
        fields = ['username', 'password']