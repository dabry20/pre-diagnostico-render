# Generated by Django 5.0.7 on 2024-10-05 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediagnostico', '0014_remove_historial_idencuesta_encuesta_idhistorial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='correo',
            field=models.EmailField(max_length=50, null=True),
        ),
    ]