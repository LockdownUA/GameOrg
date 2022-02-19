from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOISES = (
    ('PLAY', 'PLAY'),
    ('WILL PLAY', 'WILL PLAY'),
    ('ENDED', 'ENDED'),
    ('DROP', 'DROP')
)

class Genre(models.Model):
    '''Жанри наших елементів'''
    name = models.CharField(max_length=50, blank=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'
        ordering = ['name']

# Create your models here.
class Item(models.Model):
    '''Наші елементи'''
    name = models.CharField(max_length=100, blank=False)
    desc = models.TextField(max_length=350, blank=True)
    genre = models.ManyToManyField(Genre, related_name='items')
    status = models.CharField(choices=STATUS_CHOISES, max_length=50, default=STATUS_CHOISES[0])
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.profile.user.username} - {self.created.strftime("%d.%m.%y %H:%M")}'

    def get_genre(self):
        return self.genre.all()

    class Meta:
        verbose_name = 'Елемент'
        verbose_name_plural = 'Елементи'
        ordering = ['name']

class Profile(models.Model):
    '''Модель профілю'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'