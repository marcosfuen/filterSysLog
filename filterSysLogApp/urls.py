from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from filterSysLogApp import views

app_name = 'filterSysLogApp'


urlpatterns = [
    path('', admin.site.urls),
    path('login/', admin.site.urls),
    path('admin/', admin.site.urls),
    # path('admin/', admin.site.urls),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    # path('', views.profile, name='profile'),
    # path('accounts/profile/', views.profile, name='profile'),
    # path('noAutenticate/', views.noAutenticate, name='noAutenticate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
