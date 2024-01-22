"""
URL configuration for rockin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from crudapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contacts/', views.IndexView.as_view(), name='index'),
    path('contacts/<int:pk>/', views.ContactDetailView.as_view(), name='detail'),
    path('contacts/edit/<int:pk>/', views.edit, name='edit'),
    path('contacts/create/', views.create, name='create'),
    path('contacts/delete/<int:pk>/', views.delete, name='delete'),
    path('wells/create/', views.WellFormView.as_view(), name='well_create'),
    path('cores/create/', views.CoreFormView.as_view(), name='core_form'), # THIS NEEDS TO BE REMOVED IS REDNDANT
    path('wells/', views.WellListView.as_view(), name='well_list'),
    path('wells/<int:pk>/samples/create/', views.SampleFormView.as_view(), name='create_sample'),
    path('wells/<int:pk>/', views.CoreNumberSelectView.as_view(), name='select_core_number'),
    path('wells/<int:pk>/cores/create/', views.CoreFormView.as_view(), name='core_form'),
    path('wells/<int:pk>/corechips/create/', views.CoreChipFormView.as_view(), name='corechips'),
    path('wells/<int:pk>/corechips/select/', views.CoreChipSelectView.as_view(), name='corechips_select'), # A core needs to be selected before a corechip can be created
    path('wells/<int:pk>/microcores/create/', views.MicroCoreFormView.as_view(), name='microcores'),
]
