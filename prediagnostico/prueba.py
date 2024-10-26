import joblib

# Cargar el modelo
modelo_decision_tree = joblib.load('DecisionTree_modelo.pkl')
modelo_random_forest = joblib.load('RandomForest_modelo.pkl')

def predecir_dengue(modelo, valores_nuevos):
    # Realiza la predicción
    prediccion = modelo.predict([valores_nuevos])
    return prediccion

# Valores de entrada para la predicción (ejemplo)
# Asegúrate de que el orden de los valores coincida con el orden usado para entrenar el modelo
valores_nuevos = [1, 0, 1, 1, 0, 1, 0, 1, 0]  # Reemplaza con los valores que deseas probar

# Realizar predicción con el modelo Decision Tree
resultado_dt = predecir_dengue(modelo_decision_tree, valores_nuevos)
print(f'Predicción (Decision Tree): {resultado_dt[0]}')

# Realizar predicción con el modelo Random Forest
resultado_rf = predecir_dengue(modelo_random_forest, valores_nuevos)
print(f'Predicción (Random Forest): {resultado_rf[0]}')





















# import os
# import joblib

# # Definición de la ruta
# modelo_path = os.path.join('C:\\Users\\USER\\Desktop\\proydjango\\proytesis', 'DecisionTree_modelo.pkl')

# # Cargar el modelo
# try:
#     modelo = joblib.load(modelo_path)
#     print("Modelo cargado exitosamente.")
# except FileNotFoundError:
#     print(f"El archivo no se encontró en la ruta: {modelo_path}")
# except Exception as e:
#     print(f"Ocurrió un error al cargar el modelo: {e}")