# Generated by Django 5.0.7 on 2024-09-14 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediagnostico', '0012_alter_encuesta_pregunta3'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuesta',
            name='idpaciente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prediagnostico.paciente'),
        ),
    ]