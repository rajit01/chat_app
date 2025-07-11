"""
URL configuration for chat_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('chat/', include('chat.urls')),
# ]

from django.contrib import admin
from django.urls import path, include
from chat import views as chat_views

urlpatterns = [
    path('', chat_views.home, name='home'),
    path('signup/', chat_views.signup_view, name='signup'),
    path('login/', chat_views.login_view, name='login'),
    path('logout/', chat_views.logout_view, name='logout'),
    path('', include('chat.urls')),  # Note: prefixed with 'chat/'
]

