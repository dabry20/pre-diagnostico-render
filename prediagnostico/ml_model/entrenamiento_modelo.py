import pandas as pd
import tkinter as tk
from tkinter import filedialog
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

def cargar_archivo():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    archivo = filedialog.askopenfilename(title="Selecciona un archivo CSV", filetypes=[("CSV files", "*.csv")])
    return archivo

# Cargar el dataset
ruta_archivo = cargar_archivo()
if ruta_archivo:
    data = pd.read_csv(ruta_archivo)

    # Limpieza de la data 
    data = data.drop_duplicates() 
    data = data.replace('NULL', pd.NA) 
    data = data.dropna(subset=['dengue_or_not'])

    # Eliminar columnas innecesarias
    columnas_a_eliminar = [
        'dengue.p_i_d',
        'dengue.residence',
        'dengue.platelet',
        'dengue.wbc',
        'dengue._hematocri',
        'dengue.hemoglobin',
        'dengue.days',
        'dengue.date_of_fever'
    ]
    data = data.drop(columns=[col for col in columnas_a_eliminar if col in data.columns])

    # Convertir los valores de dengue.current_temp a 1 o 0
    data['current_temp'] = data['current_temp'].astype(float)
    data['current_temp'] = data['current_temp'].apply(lambda x: 1 if 100 <= x <= 105 else 0)

    for col in [
        'dengue.servere_headche', 
        'dengue.pain_behind_the_eyes', 
        'dengue.joint_muscle_aches', 
        'dengue.metallic_taste_in_the_mouth', 
        'dengue.appetite_loss', 
        'dengue.addominal_pain', 
        'dengue.nausea_vomiting', 
        'dengue.diarrhoea', 
        'dengue_or_not'
    ]:
        data[col] = data[col].map({'yes': 1, 'no': 0})

    # Preparar los datos para el modelo
    X = data[['current_temp', 'dengue.servere_headche', 'dengue.pain_behind_the_eyes', 
                'dengue.joint_muscle_aches', 'dengue.metallic_taste_in_the_mouth', 
                'dengue.appetite_loss', 'dengue.addominal_pain', 'dengue.nausea_vomiting', 
                'dengue.diarrhoea']]
    y = data['dengue_or_not']

    # Dividir el dataset en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Definir los modelos a entrenar
    modelos = {
        'DecisionTree': DecisionTreeClassifier(random_state=42),
        'RandomForest': RandomForestClassifier(random_state=42)
    }

    # Entrenar y evaluar cada modelo
    for nombre, modelo in modelos.items():
        # Validar si el modelo se puede ajustar
        try:
            modelo.fit(X_train, y_train)  # Entrenar el modelo
        except Exception as e:
            print(f"Error al entrenar el modelo {nombre}: {e}")
            continue
        
        # Validación cruzada de 20 pliegues
        scores_accuracy = cross_val_score(modelo, X_train, y_train, cv=20, scoring='accuracy')
        scores_f1 = cross_val_score(modelo, X_train, y_train, cv=20, scoring='f1')

        # Predicciones y matriz de confusión
        y_pred = modelo.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)

        # Calcular sensibilidad y especificidad
        tn, fp, fn, tp = cm.ravel()
        sensibilidad = tp / (tp + fn) if (tp + fn) > 0 else 0
        especificidad = tn / (tn + fp) if (tn + fp) > 0 else 0

        print(f'Modelo: {nombre}')
        print(f'Precisión media (20 pliegues): {scores_accuracy.mean():.2f} ± {scores_accuracy.std():.2f}')
        print(f'Puntuación F1 media (20 pliegues): {scores_f1.mean():.2f} ± {scores_f1.std():.2f}')
        print(f'Sensibilidad: {sensibilidad:.2f}')
        print(f'Especificidad: {especificidad:.2f}')
        predicciones = modelo.predict(X_test)
        resultados = pd.DataFrame({'Actual': y_test, 'Predicción': predicciones})
        print(resultados)
        # Visualizar la matriz de confusión
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Negativo', 'Positivo'], yticklabels=['Negativo', 'Positivo'])
        plt.ylabel('Actual')
        plt.xlabel('Predicción')
        plt.title(f'Matriz de Confusión - {nombre}')
        plt.show()

        # Guardar el modelo entrenado
        joblib.dump(modelo, f'{nombre}_modelo.pkl')
        print(f'Modelo {nombre} guardado como {nombre}_modelo.pkl.')




