# Generated by Django 5.0.7 on 2024-10-05 17:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediagnostico', '0016_paciente_token_paciente_token_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='correo',
            field=models.EmailField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='token_expires',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 5, 18, 7, 27, 855724, tzinfo=datetime.timezone.utc)),
        ),
    ]
