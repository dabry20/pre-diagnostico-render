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
    current_temp = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Fiebre alta repentina'  # Label personalizado
    )
    servere_headche = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Fuerte dolor de cabeza'  # Label personalizado
    )
    pain_behind_the_eyes = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Dolor y cansancio de ojos'  # Label personalizado
    )
    joint_muscle_aches = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Dolores musculares'  # Label personalizado
    )
    metallic_taste_in_the_mouth = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Sabor metálico en la boca'  # Label personalizado
    )
    appetite_loss= forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Perdida de apetito'  # Label personalizado
    )

    addominal_pain = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Dolor abdominal intenso'  # Label personalizado
    )
    nausea_vomiting = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Nauseas y vómitos'  # Label personalizado
    )
    diarrhoea = forms.BooleanField(
        required=False,  # Asegúrate de que el campo no sea obligatorio
        label='Diarrea'  # Label personalizado
    )

    class Meta:
        model = Examen
        fields = ['fsintomas', 'current_temp', 'servere_headche', 'pain_behind_the_eyes', 'joint_muscle_aches',
                    'metallic_taste_in_the_mouth', 'appetite_loss', 'addominal_pain','nausea_vomiting', 'diarrhoea','otros']
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