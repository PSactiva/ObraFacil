from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Obra",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=200)),
                ("cliente", models.CharField(max_length=200)),
                ("endereco", models.CharField(blank=True, max_length=300)),
                ("status", models.CharField(choices=[("planejada", "Planejada"), ("em_andamento", "Em andamento"), ("concluida", "Concluída"), ("pausada", "Pausada")], default="planejada", max_length=20)),
                ("data_inicio", models.DateField(blank=True, null=True)),
                ("previsao_conclusao", models.DateField(blank=True, null=True)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Obra",
                "verbose_name_plural": "Obras",
                "ordering": ["-criado_em"],
            },
        ),
    ]