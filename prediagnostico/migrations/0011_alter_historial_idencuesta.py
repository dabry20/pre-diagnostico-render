# Generated by Django 5.0.7 on 2024-09-11 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediagnostico', '0010_rename_idpaciente_examen_pkpaciente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historial',
            name='idencuesta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prediagnostico.encuesta'),
        ),
    ]