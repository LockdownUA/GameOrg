from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from .forms import LoginForm, RegForm, ItemForm
from app.models import Genre, Profile, Item

class ItemsMixin:
    status = None
    template = None

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        form = ItemForm(request.POST or None)
        items = Item.objects.filter(Q(profile__user=request.user) & Q(status=self.status))
        play_count = Item.objects.filter(Q(profile__user=request.user) & Q(status='PLAY')).count()
        will_count = Item.objects.filter(Q(profile__user=request.user) & Q(status='WILL PLAY')).count()
        ended_count = Item.objects.filter(Q(profile__user=request.user) & Q(status='ENDED')).count()
        drop_count = Item.objects.filter(Q(profile__user=request.user) & Q(status='DROP')).count()
        context = {
            'form' : form,
            'items' : items,
            'status' : self.status,
            'play_count' : play_count,
            'will_count' : will_count,
            'ended_count' : ended_count,
            'drop_count' : drop_count,
        }
        return render(request, self.template, context)

class ActionMixin:
    status = None

    def get(self, request, id):
        item = Item.objects.get(Q(id=id))
        item.status=self.status
        item.save()
        return redirect(request.META.get('HTTP_REFERER'))

# Create your views here.
class HomeView(ItemsMixin, View):
    status = 'PLAY'
    template = 'main/home.html'

class WillView(ItemsMixin, View):
    status = 'WILL PLAY'
    template = 'main/home.html'

class EndedView(ItemsMixin, View):
    status = 'ENDED'
    template = 'main/home.html'

class DropView(ItemsMixin, View):
    status = 'DROP'
    template = 'main/home.html'

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

class LoginView(View):
    def get(self, request):
        template = 'main/login.html'
        form = LoginForm(request.POST or None)
        context = {
            'form' : form,
        }
        return render(request, template, context)
    def post(self, request):
        template = 'main/login.html'
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form' : form,
        }
        return render(request, template, context)

class RegView(View):
    def get(self, request):
        template = 'main/reg.html'
        form = RegForm(request.POST or None)
        context = {
            'form' : form,
        }
        return render(request, template, context)

    def post(self, request):
        template = 'main/reg.html'
        form = RegForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(
                user=new_user,
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form' : form,
        }
        return render(request, template, context)

# Добавляємо елемент в базу        
def item_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        status = request.POST.get('status')
        genre = request.POST.getlist('genre')
        profile = Profile.objects.get(user=request.user)
        this_item = Item.objects.create(
            name=name,
            desc=desc,
            status=status,
            profile=profile,
        )
        for g in genre:
            this_item.genre.add(Genre.objects.get(id=g))
        this_item.save()
        return redirect(request.META.get('HTTP_REFERER'))

class PlayAdd(ActionMixin, View):
    status='PLAY'

class WillAdd(ActionMixin, View):
    status='WILL PLAY'

class EndedAdd(ActionMixin, View):
    status='ENDED'

class DropAdd(ActionMixin, View):
    status='DROP'

# Видаляємо елемент з бази
def delete(request, id):
    item = Item.objects.get(id=id).delete()
    item.save()
    return redirect(request.META.get('HTTP_REFERER'))