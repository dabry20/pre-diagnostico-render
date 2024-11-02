from django import forms
from .models import Paciente
from.models import Examen
from.models import Encuesta
  
class PacienteForm(forms.ModelForm):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    genero = forms.ChoiceField(
        choices=GENERO_CHOICES,
        widget=forms.Select(attrs={'style': 'font-size: 30px; font-weight: bold; background-color: #053b74ad; font-family: Times New Roman, Times, serif; color:white;'}),
        required=True
    )

    class Meta:
        model = Paciente
        fields = ['nombre', 'apePaterno', 'apeMaterno', 'documento', 'fnacimiento', 'correo', 'contra', 'genero', 'edad']
        widgets = {
            'fnacimiento': forms.DateInput(attrs={'type': 'date'}),
            'contra': forms.PasswordInput(attrs={'type': 'password'}),
            'documento': forms.TextInput(attrs={
                'pattern': '^[0-9]{8}$',  # Solo 8 dígitos
                'inputmode': 'numeric',   # Mostrar teclado numérico
                'maxlength': '8',          # Limitar a 8 caracteres
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")',
                'title': 'Ingrese exactamente 8 números'
            })
        }

class ExamenForm(forms.ModelForm):
    fsintomas = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha inicial de los síntomas:'  # Label personalizado
    )
    Fiebre = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Fiebre alta repentina'  # Label personalizado
    )
    Dolor_articulaciones = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Dolor de articulaciones'  # Label personalizado
    )
    Dolor_detras_de_ojos = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Dolor y cansancio de ojos'  # Label personalizado
    )
    Dolor_muscular = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Dolores musculares'  # Label personalizado
    )
    Dolor_de_cabeza = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Dolor de cabeza'  # Label personalizado
    )
    Erupcion_cutanea_sarpullido= forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Erupcion cutanea o sarpullido'  # Label personalizado
    )

    Nauseas_vomitos = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Nuaseas y vómitos'  # Label personalizado
    )
    Dolor_abdominal_intenso = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Dolor abdominal intenso'  # Label personalizado
    )
    Vomitos_persistentes = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Vomitos persistentes'  # Label personalizado
    )
    Sangrado_mucosas_y_encias = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Sangrado de mucosas o encias'  # Label personalizado
    )
    Somnolencia_irritabilidad = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Somnolencia o irritación'  # Label personalizado
    )
    Decaimiento = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Decaimiento'  # Label personalizado
    )

    class Meta:
        model = Examen
        fields = ['fsintomas', 'Fiebre', 'Dolor_articulaciones', 'Dolor_detras_de_ojos', 'Dolor_muscular',
                    'Dolor_de_cabeza', 'Erupcion_cutanea_sarpullido', 'Nauseas_vomitos','Dolor_abdominal_intenso',
                    'Vomitos_persistentes', 'Sangrado_mucosas_y_encias', 'Somnolencia_irritabilidad','Decaimiento','otros']
        widgets = {
            # 'idpaciente': forms.HiddenInput(), ocula los campos 
            'fsintomas': forms.DateInput(attrs={'type': 'date'}),
            
            'otros': forms.Textarea(attrs={
                'placeholder': 'Escribe aquí otros síntomas relacionados al dengue...',
                'rows': 3,
                'cols': 40,
                'style': 'resize:none; font-size: 20px; background-color: rgba(255, 255, 255, 0.5);'  # Para evitar el cambio de tamaño
            })
        }

class EncuestaForm (forms.ModelForm):
    pregunta1 = forms.BooleanField(
        label='si'  # Label personalizado
    )
    pregunta2 = forms.BooleanField(
        label='si'  # Label personalizado
    )
    pregunta3 = forms.CharField(
        label=''  # Label personalizado
    )
    class Meta:
        model= Encuesta
        fields=['pregunta1','pregunta2','pregunta3']