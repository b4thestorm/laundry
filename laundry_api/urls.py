"""laundry_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from machines.views import (
    machine_collection,
    set_machine_usage,
    set_expired,
    machines_remaining,
    save_push_token,
    registration_view,
    CustomAuthToken,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register", registration_view, name="register"),
    path("api-token-auth/", CustomAuthToken.as_view()),
    # path("login", obtain_auth_token, name="login"),
]

urlpatterns += [
    url(r"^api/v1/save-push-token/$", save_push_token, name="save_push_token"),
    url(r"^api/v1/machine_collection/$", machine_collection, name="machine_collection"),
    url(r"^api/v1/available_machines/$", set_machine_usage, name="set_machine_usage"),
    url(r"^api/v1/machines_remaining/$", machines_remaining, name="machines_remaining"),
    url(r"^api/v1/set_expired/$", set_expired, name="set_expired"),
]
