"""foodgram URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index_view, name='index'),
    path('recipes/', include('api.urls')),
    path('purchases', views.shopping_list_view, name='shopping_list'),
    path('purchases/<int:id>/', views.shopping_list_item_delete,
         name='shoplist_delete'),
    path('purchases/download/', views.shopping_list_download_view,
         name='shoplist_download'),
    path('favorites', views.favorite_recipe_view, name='favorites'),
    path('favorites/<int:id>/', views.favorite_item_delete,
         name='favorite_delete'),
    path('profile/<slug:slug>/', views.profile_view, name='profile'),
    path('subscriptions', include('users.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
