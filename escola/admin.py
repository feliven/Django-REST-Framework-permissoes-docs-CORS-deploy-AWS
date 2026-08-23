from django.contrib import admin
from django.db import models
from django.db.models.functions import Lower
from escola.models import Estudante, Curso, Matricula


# Register your models here.
class CaseInsensitiveOrderingAdmin(admin.ModelAdmin):
    def get_ordering(self, request):
        ordering = super().get_ordering(request)
        if not ordering:
            return ordering

        result = []
        for field in ordering:
            if not isinstance(field, str):
                result.append(field)
                continue

            descending = field.startswith("-")
            clean_field = field.lstrip("-")

            try:
                model_field = self.model._meta.get_field(clean_field)
                is_text = isinstance(model_field, (models.CharField, models.TextField))
            except Exception:
                is_text = False

            if is_text:
                expr = Lower(clean_field)
                result.append(expr.desc() if descending else expr.asc())
            else:
                result.append(field)

        return result


class ListandoEstudantes(CaseInsensitiveOrderingAdmin):
    list_display = ("id", "nome", "email")
    list_display_links = ("id", "nome")
    search_fields = ("nome", "cpf")
    ordering = ("nome",)
    list_editable = ("email",)
    list_per_page = 10


class ListandoCursos(CaseInsensitiveOrderingAdmin):
    list_display = ("codigo", "descricao", "nivel")
    list_display_links = ("codigo",)
    search_fields = ("codigo", "descricao")
    list_filter = ("nivel",)
    list_editable = ("nivel",)
    list_per_page = 10
    ordering = ("descricao",)


class ListandoMatriculas(CaseInsensitiveOrderingAdmin):
    list_display = ("estudante", "curso", "periodo")
    list_display_links = ("estudante", "curso")
    search_fields = ("codigo",)
    list_filter = ("periodo",)
    list_editable = ("periodo",)
    list_per_page = 10


admin.site.register(Estudante, ListandoEstudantes)
admin.site.register(Curso, ListandoCursos)
admin.site.register(Matricula, ListandoMatriculas)
