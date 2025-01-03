# Generated by Django 5.0.7 on 2024-11-01 14:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediagnostico', '0020_alter_paciente_apematerno_alter_paciente_apepaterno_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examen',
            old_name='addominal_pain',
            new_name='Dolor_abdominal_intenso',
        ),
        migrations.RenameField(
            model_name='examen',
            old_name='appetite_loss',
            new_name='Dolor_articulaciones',
        ),
        migrations.RenameField(
            model_name='examen',
            old_name='current_temp',
            new_name='Dolor_de_cabeza',
        ),
        migrations.RenameField(
            model_name='examen',
            old_name='diarrhoea',
            new_name='Dolor_detras_de_ojos',
        ),
        migrations.RenameField(
            model_name='examen',
            old_name='joint_muscle_aches',
            new_name='Dolor_muscular',
        ),
        migrations.RenameField(
            model_name='examen',
            old_name='metallic_taste_in_the_mouth',
            new_name='Erupcion_cutanea_sarpullido',
        ),
        migrations.RenameField(
            model_name='examen',
            old_name='nausea_vomiting',
            new_name='Fiebre',
        ),
        migrations.RenameField(
            model_name='examen',
            old_name='pain_behind_the_eyes',
            new_name='Nauseas_vomitos',
        ),
        migrations.RenameField(
            model_name='examen',
            old_name='resultado',
            new_name='Resultado',
        ),
        migrations.RemoveField(
            model_name='examen',
            name='servere_headche',
        ),
        migrations.AddField(
            model_name='examen',
            name='Decaimiento',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='examen',
            name='Sangrado_mucosas_y_encias',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='examen',
            name='Somnolencia_irritabilidad',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='examen',
            name='Vomitos_persistentes',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='token_expires',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 1, 15, 16, 41, 83172, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
