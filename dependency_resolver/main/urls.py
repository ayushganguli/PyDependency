"""calendar_class URL Configuration
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
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'main'

urlpatterns = [
    #auth views
    path('',views.home,name='home'),
    path('dependency_resolver_page/', views.dependency_resolver_page, name='dependency_resolver_page'),
    path('get_all_dependency_api/', views.get_all_dependency_api, name='get_all_dependency_api'),
    path('save_venv_path_api/', views.save_path_api, name='save_venv_path_api'),
    path('get_package_requirements_api/', views.get_package_requirements_api,name='get_package_requirements_api'),
    path('resolve_dependencies_api/', views.resolve_dependencies_api, name='resolve_dependencies_api')
]