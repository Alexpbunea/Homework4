import os
import json
import shutil

# Ruta de la carpeta 'extraction' (se encuentra en el mismo directorio que el script)
source_folder = 'extraction'

# Nombre de la carpeta de salida donde se guardarán los archivos válidos
output_folder = '3_table_extraction'

# Asegúrate de que la carpeta de salida exista, si no, la crea
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Función para verificar si un archivo JSON contiene al menos 3 tablas
def contains_at_least_three_tables(json_data):
    # Contar cuántas claves corresponden a tablas, por ejemplo: 'id_table_1', 'id_table_2', etc.
    # Esto puede cambiar si el formato de las claves varía
    table_keys = [key for key in json_data.keys() if key.startswith('id_table_')]
    return len(table_keys) >= 3

# Lista para almacenar los archivos válidos
valid_files = []

# Buscar archivos JSON en la carpeta 'extraction'
for filename in os.listdir(source_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(source_folder, filename)
        
        # Leer el contenido del archivo JSON
        with open(filepath, 'r', encoding='utf-8') as file:
            try:
                json_data = json.load(file)
                
                # Si el archivo contiene al menos 3 tablas, agregarlo a la lista de archivos válidos
                if contains_at_least_three_tables(json_data):
                    valid_files.append(filepath)
                
            except json.JSONDecodeError:
                print(f"Error al leer el archivo JSON: {filename}")

# Si encontramos al menos 10 archivos válidos, los copiamos a la nueva carpeta
if len(valid_files) >= 10:
    for i in range(10):
        # Copiar el archivo válido a la carpeta de salida
        shutil.copy(valid_files[i], os.path.join(output_folder, f'valid_extraction_{i+1}.json'))
    print(f"Se han copiado 10 archivos válidos a la carpeta '{output_folder}'.")
else:
    print(valid_files)
    print("No se encontraron suficientes archivos con al menos 3 tablas.")
