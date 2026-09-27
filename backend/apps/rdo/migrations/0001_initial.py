import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("obras", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="DiarioObra",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("data", models.DateField()),
                ("clima", models.CharField(choices=[("ensolarado", "Ensolarado"), ("nublado", "Nublado"), ("chuvoso", "Chuvoso"), ("parcial", "Parcialmente nublado")], max_length=20)),
                ("temperatura", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("ocorrencias", models.TextField(blank=True)),
                ("atividades", models.TextField(blank=True)),
                ("efetivo", models.PositiveIntegerField(default=0)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("criado_por", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="diarios_obra", to=settings.AUTH_USER_MODEL)),
                ("obra", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="diarios", to="obras.obra")),
            ],
            options={"ordering": ["-data", "-criado_em"], "verbose_name": "Diário de Obra", "verbose_name_plural": "Diários de Obra"},
        ),
        migrations.CreateModel(
            name="FotoDiario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("imagem", models.ImageField(upload_to="rdo/%Y/%m/")),
                ("legenda", models.CharField(blank=True, max_length=200)),
                ("enviada_em", models.DateTimeField(auto_now_add=True)),
                ("diario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="fotos", to="rdo.diarioobra")),
            ],
            options={"ordering": ["enviada_em"]},
        ),
        migrations.AddConstraint(model_name="diarioobra", constraint=models.UniqueConstraint(fields=("obra", "data"), name="unique_diario_por_obra_data")),
    ]
