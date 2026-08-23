"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from escola.views import (
    EstudanteViewSet,
    CursoViewSet,
    MatriculaViewSet,
    MatriculasPorEstudante,
    MatriculasPorCurso,
)

router = routers.DefaultRouter()
router.register(r"estudantes", EstudanteViewSet)
router.register(r"cursos", CursoViewSet)
router.register(r"matriculas", MatriculaViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("estudantes/<int:pk>/matriculas", MatriculasPorEstudante.as_view()),
    path("cursos/<int:pk>/matriculas", MatriculasPorCurso.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
