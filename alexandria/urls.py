"""
URL configuration for alexandria project.

The `urlpatterns` list routes URLs to Home.as_view() more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from alexandria.views.home import Home
from alexandria.views.explore import Explore
from alexandria.views.auth import SigninView, LoginView, ProcessLogin, ProcessSignin, LogoutView
from alexandria.views.profile import ProfileView


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('explorar/', Explore.as_view(), name='explorar'),
    path('como-funciona/', Home.as_view(), name='como-funciona'),
    path('comunidade/', Home.as_view(), name='comunidade'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('auth/login/', ProcessLogin.as_view(), name='auth_login'),
    path('auth/signin/', ProcessSignin.as_view(), name='auth_signin'),
    path('perfil/', ProfileView.as_view(), name='perfil'),
    path('regioes/', Home.as_view(), name='regioes'),
    path('regiao/<str:regiao>/', Home.as_view(), name='livros-por-regiao'),
    path('termos/', Home.as_view(), name='termos'),
    path('privacidade/', Home.as_view(), name='privacidade'),
    path('suporte/', Home.as_view(), name='suporte'),
]
