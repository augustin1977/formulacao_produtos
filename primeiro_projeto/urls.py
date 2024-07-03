"""
URL configuration for primeiro_projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views
import produtos.views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("cadastrarproduto/", produtos.views.cadastrarproduto , name="cadastrarproduto"),
    path('', produtos.views.home, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/',produtos.views.logoutUser,name='logout_user'),
    path('lista_produtos/',produtos.views.lista_produtos,name='lista_produtos'),
    path('editarproduto/<int:produto_id>/', produtos.views.editar_produto, name='editarproduto'),
]
urlpatterns+=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
