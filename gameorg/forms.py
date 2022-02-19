from cProfile import label
from unicodedata import name
from django import forms
from django.contrib.auth.models import User
from app.models import Item, Genre

class LoginForm(forms.ModelForm):
    '''Форма авторизації'''
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Користувача з логіном {username} не існує')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Не правильний пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']

class RegForm(forms.ModelForm):
    '''Форма реєстрації'''
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Підтвердіть пароль'
        self.fields['email'].label = 'Електронная пошта'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Даний email уже зареєстрований в системі')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Ім'я {username} занято")
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Паролі не співпадають')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']

class ItemForm(forms.ModelForm):
    '''Форма для добавлення елементу в базу даних'''
    genre = forms.ModelMultipleChoiceField(
        label='Жанри',
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Item
        fields = ['name', 'desc', 'genre', 'status']
        labels = {
            'name' : 'Назва',
            'desc' : 'Опис',
            'status' : 'Статус',
        }