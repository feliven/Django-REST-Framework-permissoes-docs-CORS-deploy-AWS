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
from django.views.generic import RedirectView
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
    path("", RedirectView.as_view(url="/v1/", permanent=False)),
    # Schemas para v1 e v2
    path("schema/v1/", SpectacularAPIView.as_view(api_version="v1"), name="schema-v1"),
    path("schema/v2/", SpectacularAPIView.as_view(api_version="v2"), name="schema-v2"),
    # Swagger UI único (com seletor)
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema-v1"),
        name="swagger-ui",
    ),
    # Rotas da API
    path("<str:version>/", include(router.urls)),
    path(
        "<str:version>/estudantes/<int:pk>/matriculas",
        MatriculasPorEstudante.as_view(),
    ),
    path(
        "<str:version>/cursos/<int:pk>/matriculas",
        MatriculasPorCurso.as_view(),
    ),
]
