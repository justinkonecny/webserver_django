"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include

from recommendations.urls import urlpatterns as recommendation_urls
from spotify.urls import urlpatterns as spotify_urls
from users.urls import urlpatterns as users_urls
from base.urls import urlpatterns as base_urls
from groups.urls import urlpatterns as groups_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', include(base_urls)),
    path('users/', include(users_urls)),
    path('spotify/', include(spotify_urls)),
    path('recommendations/', include(recommendation_urls)),
    path('groups/', include(groups_urls)),
]
