"""gameorg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from .views import (
    HomeView,
    WillView,
    EndedView,
    DropView,
    item_add,
    PlayAdd,
    WillAdd,
    EndedAdd,
    DropAdd,
    delete,
    logout_view,
    LoginView,
    RegView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('will-play/', WillView.as_view(), name='will-play'),
    path('ended/', EndedView.as_view(), name='ended'),
    path('drop/', DropView.as_view(), name='drop'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('add-item/', item_add, name='add-item'),
    path('delete-item/<int:id>/', delete, name='del-item'),
    path('add-play/<int:id>/', PlayAdd.as_view(), name='add-play'),
    path('add-will/<int:id>/', WillAdd.as_view(), name='add-will'),
    path('add-ended/<int:id>/', EndedAdd.as_view(), name='add-ended'),
    path('add-drop/<int:id>/', DropAdd.as_view(), name='add-drop'),
]
