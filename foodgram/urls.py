from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
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
    path('subscriptions', views.subscriptions_index, name='subscriptions'),
    path('subscriptions/<int:id>/follow/', views.follow_view, name='follows'),
    path('subscriptions/<int:id>/unfollow/', views.unfollow_view,
         name='unfollow'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
