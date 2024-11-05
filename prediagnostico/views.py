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
from datetime import date, datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import uuid
from django.shortcuts import render
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

    # Obtener las fechas y el resultado desde el formulario GET
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    resultado = request.GET.get('resultado')

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
                    idhistorial=historial_instance,
                    pregunta1=form.cleaned_data['pregunta1'],
                    pregunta2=form.cleaned_data['pregunta2'],
                    pregunta3=form.cleaned_data['pregunta3']
                )
                respuesta.save()

                # Redirigir o mostrar un mensaje de éxito
                return redirect('Historial')

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
                pass

        # Aplicar filtro por resultado si está presente
        if resultado:
            historiales = historiales.filter(idexamen__Resultado=resultado)

        # Limitar a los últimos 15 resultados
        datos_historial = []
        total_dias = 0
        count = 0

        for historial in historiales.order_by('-idhistorial')[:15]:
            FIS = historial.idexamen.fsintomas
            FD = historial.idexamen.created

            # Convertir a offset-naive
            if isinstance(FIS, date):
                FIS = datetime.combine(FIS, datetime.min.time())
            if FD.tzinfo is not None:
                FD = FD.replace(tzinfo=None)  # Hacer FD offset-naive

            tiempo_deteccion = (FD - FIS).days

            if tiempo_deteccion >= 0:  # Asegurarse de que la diferencia sea válida
                total_dias += tiempo_deteccion
                count += 1

            # Se agrega el tiempo de detección al diccionario, pero tdd se calculará después
            datos_historial.append({
                'id': historial.idhistorial,
                'Fexamen': FD.strftime('%d/%m/%Y'),
                'Resultado': historial.idexamen.Resultado,
                'Fiebre': historial.idexamen.Fiebre,
                'darticulaciones': historial.idexamen.Dolor_articulaciones,
                'dojos': historial.idexamen.Dolor_detras_de_ojos,
                'dmuscular': historial.idexamen.Dolor_muscular,
                'dcabeza': historial.idexamen.Dolor_de_cabeza,
                'Ecutanea': historial.idexamen.Erupcion_cutanea_sarpullido,
                'nauseas': historial.idexamen.Nauseas_vomitos,
                'dabdominal_intenso': historial.idexamen.Dolor_abdominal_intenso,
                'vomitos_persistentes': historial.idexamen.Vomitos_persistentes,
                'sangradomucosas': historial.idexamen.Sangrado_mucosas_y_encias,
                'somnolencia': historial.idexamen.Somnolencia_irritabilidad,
                'Decaimiento': historial.idexamen.Decaimiento,
                'otros': historial.idexamen.otros,
                'tiempo': tiempo_deteccion,  # Guardar el tiempo de detección correspondiente
                'test_realizado': Encuesta.objects.filter(idpaciente=paciente, idhistorial=historial).exists()
            })

        num_dengue_grave = historiales.filter(idexamen__Resultado='3').count()
        num_personas_detectadas = historiales.count()

        # Calcular el Tiempo Promedio de Detección del Dengue (TDD)
        tdd = total_dias / count if count > 0 else 0
    else:
        datos_historial = []
        num_dengue_grave = 0
        num_personas_detectadas = 0
        tdd = 0

    return render(request, "prediagnostico/historial.html", {
        'datos_historial': datos_historial,
        'form': form,
        'fecha_desde': request.GET.get('fecha_desde', ''),
        'fecha_hasta': request.GET.get('fecha_hasta', ''),
        'resultado': request.GET.get('resultado', ''),
        'num_dengue_grave': num_dengue_grave,
        'num_personas_detectadas': num_personas_detectadas,
        'tdd': tdd,  # tdd ahora se calcula correctamente
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
import os
import pandas as pd
import joblib
from django.shortcuts import render
from django.contrib import messages
from .forms import ExamenForm
from .models import Paciente
import time 

def home(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)

        if form.is_valid():
            documento = request.session.get('docu')
            try:
                paciente = Paciente.objects.get(documento=documento)
                form.instance.paciente = paciente

                # Recopilar datos del formulario
                datos = {
                    'Fiebre': 1 if 'Fiebre' in request.POST else 0,
                    'Dolor_articulaciones': 1 if 'Dolor_articulaciones' in request.POST else 0,
                    'Dolor_detras_de_ojos': 1 if 'Dolor_detras_de_ojos' in request.POST else 0,
                    'Dolor_muscular': 1 if 'Dolor_muscular' in request.POST else 0,
                    'Dolor_de_cabeza': 1 if 'Dolor_de_cabeza' in request.POST else 0,
                    'Erupcion_cutanea_sarpullido': 1 if 'Erupcion_cutanea_sarpullido' in request.POST else 0,
                    'Nauseas_vomitos': 1 if 'Nauseas_vomitos' in request.POST else 0,
                    'Dolor_abdominal_intenso': 1 if 'Dolor_abdominal_intenso' in request.POST else 0,
                    'Vomitos_persistentes': 1 if 'Vomitos_persistentes' in request.POST else 0,
                    'Sangrado_mucosas_y_encias': 1 if 'Sangrado_mucosas_y_encias' in request.POST else 0,
                    'Somnolencia_irritabilidad': 1 if 'Somnolencia_irritabilidad' in request.POST else 0,
                    'Decaimiento': 1 if 'Decaimiento' in request.POST else 0,
                }

                # Cargar el modelo
                current_dir = os.path.dirname(__file__)
                modelo_path = os.path.join(current_dir, 'models', 'modelo_bosque_aleatorio.pkl')

                try:
                    modelo = joblib.load(modelo_path)
                except FileNotFoundError:
                    messages.error(request, 'Modelo no encontrado. Asegúrate de que el archivo exista.')
                    return render(request, 'prediagnostico/home.html', {'form': form})

                # Crear un DataFrame para la predicción
                X_nuevo = pd.DataFrame([[ 
                    datos['Fiebre'], 
                    datos['Dolor_articulaciones'], 
                    datos['Dolor_detras_de_ojos'], 
                    datos['Dolor_muscular'], 
                    datos['Dolor_de_cabeza'], 
                    datos['Erupcion_cutanea_sarpullido'], 
                    datos['Nauseas_vomitos'], 
                    datos['Dolor_abdominal_intenso'], 
                    datos['Vomitos_persistentes'], 
                    datos['Sangrado_mucosas_y_encias'], 
                    datos['Somnolencia_irritabilidad'], 
                    datos['Decaimiento']
                ]], columns=[
                    'Fiebre',
                    'Dolor_articulaciones',
                    'Dolor_detras_de_ojos',
                    'Dolor_muscular',
                    'Dolor_de_cabeza',
                    'Erupcion_cutanea_sarpullido',
                    'Nauseas_vomitos',
                    'Dolor_abdominal_intenso',
                    'Vomitos_persistentes',
                    'Sangrado_mucosas_y_encias',
                    'Somnolencia_irritabilidad',
                    'Decaimiento'
                ])

                # Iniciar el conteo del tiempo
                tiempo_inicio = time.time()

                # Realizar la predicción
                Resultado = modelo.predict(X_nuevo)

                # Finalizar el conteo del tiempo
                tiempo_fin = time.time()
                duracion_en_segundos = tiempo_fin - tiempo_inicio  # Calcular la duración

                # Modificar el mensaje según el resultado
                if Resultado[0] == 1:
                    mensaje = "Usted posiblemente no presenta dengue."
                elif Resultado[0] == 2:
                    mensaje = "Usted posiblemente presenta dengue."
                elif Resultado[0] == 3:
                    mensaje = "Usted posiblemente presenta dengue grave."
                else:
                    mensaje = "Resultado desconocido."

                # Guardar el examen con el resultado y la duración
                examen = form.save(commit=False)
                examen.pkpaciente = paciente 
                examen.Resultado = Resultado[0]  # Guardar el resultado de la predicción
                examen.Tiempo_deteccion = duracion_en_segundos  # Almacena el tiempo de detección 
                examen.save()

                messages.success(request, '¡Registro exitoso! El examen ha sido guardado correctamente.')
                form = ExamenForm()  # Reiniciar el formulario
                return render(request, 'prediagnostico/home.html', {'form': form, 'mensaje': mensaje})

            except Paciente.DoesNotExist:
                messages.error(request, 'Paciente no encontrado.')

    else:
        form = ExamenForm()

    return render(request, 'prediagnostico/home.html', {'form': form})

# -------------------------------------------------------------------------------------------------