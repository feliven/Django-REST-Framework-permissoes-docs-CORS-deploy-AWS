from django.db.models.functions import Lower
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from escola.models import Estudante, Curso, Matricula
from escola.serializers import (
    EstudanteSerializer,
    EstudanteSerializerV2,
    CursoSerializer,
    MatriculaSerializer,
    MatriculasPorEstudanteSerializer,
    MatriculasPorCursoSerializer,
)
from escola.throttles import EstudanteRateThrottle, CursoRateThrottle


class ShortPagination(PageNumberPagination):
    page_size = 10


class LongPagination(PageNumberPagination):
    page_size = 20


class CaseInsensitiveOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        # If no ordering was specified, do not modify the queryset's ordering.
        # Previously the filter always called queryset.order_by(*ordering).
        # When no ordering was supplied, it cleared any ordering
        # and produced an unordered QuerySet.
        if not ordering:
            return queryset
        ordering = [
            Lower(f[1:]).desc() if f.startswith("-") else Lower(f) for f in ordering
        ]
        return queryset.order_by(*ordering)


class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all().order_by("id")
    pagination_class = LongPagination
    filter_backends = [DjangoFilterBackend, CaseInsensitiveOrderingFilter, SearchFilter]
    ordering_fields = ["nome"]
    search_fields = ["nome", "cpf"]
    throttle_classes = [EstudanteRateThrottle]

    def get_serializer_class(self):  # type: ignore[override]
        if getattr(self.request, "version", None) == "v2":
            return EstudanteSerializerV2
        return EstudanteSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all().order_by("id")
    serializer_class = CursoSerializer
    pagination_class = ShortPagination
    throttle_classes = [CursoRateThrottle]
    permission_classes = [IsAuthenticatedOrReadOnly]


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all().order_by("id")
    serializer_class = MatriculaSerializer
    http_method_names = ["get", "post"]


class MatriculasPorEstudante(generics.ListAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculasPorEstudanteSerializer

    def get_queryset(self):  # type: ignore[override]
        queryset = Matricula.objects.filter(estudante_id=self.kwargs["pk"]).order_by(
            "id"
        )
        return queryset


class MatriculasPorCurso(generics.ListAPIView):
    queryset = Matricula.objects.all()
    serializer_class = MatriculasPorCursoSerializer

    def get_queryset(self):  # type: ignore[override]
        queryset = Matricula.objects.filter(curso_id=self.kwargs["pk"]).order_by("id")
        return queryset
