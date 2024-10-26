from django.contrib import messages
from django.shortcuts import render, redirect
from proytesis import settings
from .forms import PacienteForm
from .forms import ExamenForm
from .forms import EncuestaForm
import joblib
import os
import pandas as pd
import numpy as np
from .models import Paciente
from .models import Encuesta
from .models import Historial
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import uuid

# CREACION DE LAS VISTAS
# def login(request):
#     return render(request,"prediagnostico/login.html")


# def registro(request):
#     return render(request,"prediagnostico/registro.html")


def vista(request):
    print("Entrando a la vista de perfil")  # Para depuración
    docu = request.session.get('docu')
    if not docu:
        print("No hay documento en la sesión, redirigiendo a login.")
        return redirect('login')  # Redirigir si no hay documento

    # Obtener el paciente usando el documento
    try:
        paciente = get_object_or_404(Paciente, documento=docu)
        print(f'Datos del paciente: {paciente}')  # Para depuración
    except Exception as e:
        print(f'Error al obtener el paciente: {e}')  # Para depuración
        return redirect('login')  # Redirigir en caso de error

    return render(request, 'prediagnostico/perfil.html', {'paciente': paciente})

def Editar_paciente(request):
    if request.method == 'POST':
        docu = request.POST.get('documento')
        paciente = get_object_or_404(Paciente, documento=docu)
        
        # Actualiza los datos del paciente
        paciente.nombre = request.POST.get('nombre')
        paciente.apePaterno = request.POST.get('apePaterno')
        paciente.apeMaterno = request.POST.get('apeMaterno')
        paciente.fnacimiento = request.POST.get('fnacimiento')
        paciente.correo = request.POST.get('correo')
        
        paciente.save()  # Guarda los cambios en la base de datos
        
        return redirect('Vista')  # Redirige al perfil después de guardar cambios

    return redirect('Vista')  # Redirige si no es un POST


# LOGIN DE LA WEB---------------------------------------------------------
def login(request):
    if request.method == 'POST':
        docu = request.POST.get('id_documento')
        passw = request.POST.get('id_contra')
# Agregar impresión para depuración
        print(f'Documento ingresado: {docu}')
        print(f'Contraseña ingresada: {passw}')

        try:
            paciente = Paciente.objects.get(documento=docu)
            # Guardar el documento en la sesión
            request.session['docu'] = docu
            if check_password(passw, paciente.contra):
                # Redirigir a la página deseada después de iniciar sesión
                return redirect('Home')  # Cambia esto a tu vista deseada
            else:
                error = 'Contraseña incorrecta'
        except Paciente.DoesNotExist:
            error = 'Usuario no encontrado'

        return render(request, 'prediagnostico/login.html', {'error': error})

    return render(request, 'prediagnostico/login.html')
#-------------------------------------------------------------------------

def historial(request):
    docu = request.session.get('docu')
    form = EncuestaForm()

    # Obtener las fechas desde el formulario GET
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        historial_id = request.POST.get('historial_id')  # Obtener el ID del historial del formulario

        if form.is_valid():
            # Obtener el paciente correspondiente al documento
            paciente = get_object_or_404(Paciente, documento=docu)

            # Verificar si ya existe una encuesta para este historial
            if Encuesta.objects.filter(idpaciente=paciente, idhistorial=historial_id).exists():
                form.add_error(None, "Ya has realizado este test")
            else:
                # Obtener la instancia de Historial correspondiente al ID
                historial_instance = get_object_or_404(Historial, idhistorial=historial_id)

                # Guardar las respuestas en la base de datos
                respuesta = Encuesta(
                    idpaciente=paciente,
                    idhistorial=historial_instance,  # Asignar la instancia de Historial
                    pregunta1=form.cleaned_data['pregunta1'],
                    pregunta2=form.cleaned_data['pregunta2'],
                    pregunta3=form.cleaned_data['pregunta3']
                )
                respuesta.save()  # Guardar la respuesta

                # Redirigir o mostrar un mensaje de éxito
                return redirect('Historial')  # Cambia 'Historial' por la vista a la que deseas redirigir

    if docu:
        paciente = get_object_or_404(Paciente, documento=docu)
        historiales = Historial.objects.filter(idpaciente=paciente).select_related('idexamen')

        # Aplicar filtros de fecha si están presentes
        if fecha_desde and fecha_hasta:
            try:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
                fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
                historiales = historiales.filter(idexamen__created__range=[fecha_desde, fecha_hasta])
            except ValueError:
                pass  # Si hay un error en el formato de fecha, no aplicamos el filtro

        # Limitar a los últimos 15 resultados
        datos_historial = [
            {
                'id': historial.idhistorial,
                'fexamen': historial.idexamen.created.strftime('%d/%m/%Y'),
                'resultado': historial.idexamen.resultado,
                'fiebre': historial.idexamen.current_temp,
                'dcabeza': historial.idexamen.servere_headche,
                'dojos': historial.idexamen.pain_behind_the_eyes,
                'dmuscular': historial.idexamen.joint_muscle_aches,
                'sboca': historial.idexamen.metallic_taste_in_the_mouth,
                'papetito': historial.idexamen.appetite_loss,
                'dabdominal': historial.idexamen.addominal_pain,
                'nauseas': historial.idexamen.nausea_vomiting,
                'diarrea': historial.idexamen.diarrhoea,
                'otros': historial.idexamen.otros,
                
                'test_realizado': Encuesta.objects.filter(idpaciente=paciente, idhistorial=historial).exists()  # Verificar si ya realizó el test
            }
            for historial in historiales.order_by('-idhistorial')[:15]  # Obtener solo los últimos 15 resultados
        ]
    else:
        datos_historial = []

    return render(request, "prediagnostico/historial.html", {
        'datos_historial': datos_historial,
        'form': form,
        'fecha_desde': request.GET.get('fecha_desde', ''),
        'fecha_hasta': request.GET.get('fecha_hasta', ''),
    })


# RECUPERAR CONTRASEÑA--> ENVIAR TOKEN AL CORREO
def recuperar(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        
        # Usa filter() en lugar de get()
        pacientes = Paciente.objects.filter(correo=correo)

        if pacientes.exists():
            if pacientes.count() == 1:
                user = pacientes.first()  # Obtiene el único paciente
            else:
                # Si hay más de un registro, puedes manejarlo como prefieras
                error = 'Se encontraron múltiples registros para este correo.'
                return render(request, 'prediagnostico/recuperar.html', {'error': error})

            # Generar un token único
            token = uuid.uuid4()
            user.token = token
            user.token_expires = timezone.now() + timedelta(hours=1)  # Establecer la expiración
            user.save()  # Guardar el usuario con el nuevo token
            
            # Enviar el correo electrónico
            reset_link = f"http://localhost:8000/restablecer/{token}/"
            send_mail(
                'Recuperación de Contraseña',
                f'Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [correo],
                fail_silently=False,
            )
            success = 'Se ha enviado un correo con instrucciones para restablecer tu contraseña.'
            return render(request, 'prediagnostico/recuperar.html', {'success': success})
        
        else:
            error = 'El correo electrónico no está registrado.'
            return render(request, 'prediagnostico/recuperar.html', {'error': error})

    return render(request, 'prediagnostico/recuperar.html')
# RESTABLECER CONTRASEÑA
def restablecer(request, token):
    try:
        user = Paciente.objects.get(token=token)

        if timezone.now() > user.token_expires:
            return render(request, 'prediagnostico/restablecer.html', {'error': 'El token ha expirado.'})

        if request.method == 'POST':
            nueva_contra = request.POST.get('nueva_contra')
            confirmar_contra = request.POST.get('confirmar_contra')

            if nueva_contra != confirmar_contra:
                return render(request, 'prediagnostico/restablecer.html', {'error': 'Las contraseñas no coinciden.'})

            user.contra = nueva_contra  # Cambiar la contraseña
            user.token = None  # Limpiar el token después de restablecer
            user.token_expires = None  # Limpiar la fecha de expiración
            user.save()  # Asegúrate de que aquí no se está intentando guardar un valor nulo para token

            return redirect('login')

        return render(request, 'prediagnostico/restablecer.html', {'token': token})

    except Paciente.DoesNotExist:
        return render(request, 'prediagnostico/restablecer.html', {'error': 'Token inválido.'})


# RGISTRO DE PACIENTES --------------------------
def registro(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo paciente
            messages.success(request, '¡Registro exitoso! El paciente ha sido guardado correctamente.')
            return redirect('login')
    else:
        form = PacienteForm()
    
    return render(request, 'prediagnostico/registro.html', {'form': form})
# ------------------------------------------------------------------------------------

# ELECCION DE SINTOMAS
def home(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)

        if form.is_valid():
            # Obtener el documento del paciente desde la sesión
            documento = request.session.get('docu')
            # print(f'Documento ingresado: {documento}') 
            try:
                # Buscar el paciente usando el documento
                paciente = Paciente.objects.get(documento=documento)

                # Asignar automáticamente el id del paciente al campo idpaciente_id del formulario
                form.instance.paciente = paciente

                # Obtener los datos del formulario y transformarlos
                datos = {
                    'current_temp': 1 if 'current_temp' in request.POST else 0,
                    'servere_headche': 1 if 'servere_headche' in request.POST else 0,
                    'pain_behind_the_eyes': 1 if 'pain_behind_the_eyes' in request.POST else 0,
                    'joint_muscle_aches': 1 if 'joint_muscle_aches' in request.POST else 0,
                    'metallic_taste_in_the_mouth': 1 if 'metallic_taste_in_the_mouth' in request.POST else 0,
                    'appetite_loss': 1 if 'appetite_loss' in request.POST else 0,
                    'addominal_pain': 1 if 'addominal_pain' in request.POST else 0,
                    'nausea_vomiting': 1 if 'nausea_vomiting' in request.POST else 0,
                    'diarrhoea': 1 if 'diarrhoea' in request.POST else 0,
                }

                # imprimir los datos obtenidos
                print("Datos del formulario:", datos)

                # Cargar el modelo
                modelo_path = os.path.join('C:\\Users\\USER\\Desktop\\proydjango\\proytesis', 'RandomForest_modelo.pkl')
                modelo = joblib.load(modelo_path)

                # Preparar los datos para la predicción usando un DataFrame
                X_nuevo = pd.DataFrame([[ 
                    datos['current_temp'], 
                    datos['servere_headche'], 
                    datos['pain_behind_the_eyes'], 
                    datos['joint_muscle_aches'], 
                    datos['metallic_taste_in_the_mouth'], 
                    datos['appetite_loss'], 
                    datos['addominal_pain'], 
                    datos['nausea_vomiting'], 
                    datos['diarrhoea']
                ]], columns=[
                    'current_temp',
                    'dengue.servere_headche',
                    'dengue.pain_behind_the_eyes',
                    'dengue.joint_muscle_aches',
                    'dengue.metallic_taste_in_the_mouth',
                    'dengue.appetite_loss',
                    'dengue.addominal_pain',
                    'dengue.nausea_vomiting',
                    'dengue.diarrhoea'
                ])
                print("Datos para la predicción:", X_nuevo)

                # Hacer la predicción
                resultado = modelo.predict(X_nuevo)

                # Mensaje con el resultado de la predicción
                resultado_prediccion = resultado[0] == 1  # 1 indica positivo
                if resultado_prediccion:
                    mensaje = "Usted posiblemente esta infectado de dengue."
                else:
                    mensaje = "Usted posiblemente No esta infectado de dengue."

                # Guardar los datos en la base de datos
                examen = form.save(commit=False)  # No guardar aún
                examen.pkpaciente = paciente 
                examen.resultado = resultado_prediccion  # Guardar el resultado de la predicción
                examen.save()  # Ahora guardar el examen con la predicción
                messages.success(request, '¡Registro exitoso! El examen ha sido guardado correctamente.')
                form = ExamenForm()
                # Redirigir a la URL deseada
                return render(request, 'prediagnostico/home.html', {'form': form, 'mensaje': mensaje})

            except Paciente.DoesNotExist:
                messages.error(request, 'Paciente no encontrado.')

    else:
        form = ExamenForm()

    return render(request, 'prediagnostico/home.html', {'form': form})
# -------------------------------------------------------------------------------------------------