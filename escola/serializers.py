from rest_framework import serializers
from escola.models import Estudante, Curso, Matricula
from escola.validators import cpf_invalido, nome_invalido, celular_invalido


class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = "__all__"

    def validate(self, attrs):
        if cpf_invalido(attrs["cpf"]):
            raise serializers.ValidationError({"cpf": "CPF inválido"})
        if nome_invalido(attrs["nome"]):
            raise serializers.ValidationError(
                {"nome": "Nome deve conter apenas letras"}
            )
        if celular_invalido(attrs["numero_celular"]):
            raise serializers.ValidationError(
                {
                    "celular": "Celular precisa estar no formato 11 55555-4444, "
                    "respeitando traços e espaços"
                }
            )

        return attrs


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = []


class MatriculasPorEstudanteSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source="curso.descricao")
    periodo = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = ["curso", "periodo"]

    def get_periodo(self, obj):
        return obj.get_periodo_display()


class MatriculasPorCursoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.ReadOnlyField(source="estudante.nome")

    class Meta:
        model = Matricula
        fields = ["estudante_nome"]


class EstudanteSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ["id", "nome", "email", "numero_celular"]
