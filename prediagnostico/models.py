from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from django.utils import timezone
import uuid
# Create your models here.

class Paciente(models.Model):
    idpaciente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    apePaterno = models.CharField(max_length=50, null=True)
    apeMaterno = models.CharField(max_length=50, null=True)
    documento = models.CharField(max_length=15, unique=True)
    fnacimiento = models.DateField(blank=True, null=True)
    correo = models.EmailField(max_length=50, null=True ,unique=True)
    token = models.UUIDField(default=uuid.uuid4, null=True, editable=False)
    token_expires = models.DateTimeField(default=timezone.now() + timedelta(hours=1),null=True)
    contra = models.CharField(max_length=128)  # Asegúrate de que sea un tamaño adecuado
    genero = models.CharField(max_length=10)
    edad = models.CharField(blank=True, null=True, max_length=3)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'paciente'
        verbose_name_plural = 'pacientes'

    def __str__(self):
        return f"{self.nombre} {self.apePaterno} {self.apeMaterno}"

    def save(self, *args, **kwargs):
        if self.contra:
            self.contra = make_password(self.contra)  # Cifrar la contraseña
        super().save(*args, **kwargs)

# TABLA EXAMEN
class Examen(models.Model):
    idexamen=models.AutoField(primary_key=True)
    pkpaciente=models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True)
    fsintomas=models.DateField()
    current_temp=models.BooleanField()
    servere_headche=models.BooleanField()
    pain_behind_the_eyes=models.BooleanField()
    joint_muscle_aches=models.BooleanField()
    metallic_taste_in_the_mouth=models.BooleanField()
    appetite_loss=models.BooleanField()
    addominal_pain=models.BooleanField()
    nausea_vomiting=models.BooleanField()
    diarrhoea=models.BooleanField()
    otros=models.TextField(blank=True, null=True,max_length=300)
    resultado=models.CharField(blank=True, null=True,max_length=30)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)


#TABLA HISTORIAL
class Historial (models.Model):
    idhistorial=models.AutoField(primary_key=True)
    idpaciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)
    idexamen=models.ForeignKey(Examen, on_delete=models.CASCADE)


#TABLA ENCUESTA
class Encuesta(models.Model):
    idencuesta=models.AutoField(primary_key=True)
    idpaciente=models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True)
    idhistorial=models.ForeignKey(Historial, on_delete=models.CASCADE,  null=True)
    pregunta1=models.BooleanField()
    pregunta2=models.BooleanField()
    pregunta3=models.CharField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)