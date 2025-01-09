import os
import json
import logging
from bs4 import BeautifulSoup
import spacy

# Configuración del log
logging.basicConfig(level=logging.DEBUG)

# Cargamos un modelo de spaCy
nlp = spacy.load("en_core_web_sm")

def extract_topic(caption):
    """Extrae el tema principal de la tabla."""
    return caption.strip() if caption else "Sin tema definido"

def extract_key_value_pairs(table_data):
    """Extrae pares clave-valor de una tabla."""
    logging.debug("Extracting key-value pairs from table.")
    extracted_rows = []

    # Asumimos que la primera fila contiene encabezados
    headers = [cell.text.strip() for cell in table_data[0].find_all(["th", "td"])]

    # Procesamos las filas siguientes como contenido
    for row in table_data[1:]:
        cells = row.find_all(["th", "td"])
        values = [cell.text.strip() for cell in cells]

        if len(values) == len(headers):
            extracted_rows.append(dict(zip(headers, values)))
        else:
            logging.warning("Fila ignorada debido a longitud inconsistente con encabezados.")

    logging.debug(f"Extracted rows: {extracted_rows}")
    return extracted_rows

def generate_claims_with_spacy(rows, dataset_name, table_caption):
    """Genera claims personalizadas usando spaCy y reglas basadas en texto."""
    formatted_claims = []

    for row in rows:
        # Construimos una frase base para cada claim
        claim_parts = []
        for key, value in row.items():
            claim_parts.append(f"|{key}, {value}|")

        # Unimos los diferentes elementos de la claim
        claim_specification = ", ".join(claim_parts)
        measure = ''  # Aquí puedes incluir lógica específica si es necesario
        outcome = ''  # Lo mismo para el resultado

        # Formateamos la claim final
        formatted_claim = f"|{{{claim_specification}}}, {measure}, {outcome}|"
        formatted_claims.append(formatted_claim)

    return formatted_claims

def extract_claims_from_table(json_file, topic_filter=None):
    """Extrae claims (duplas) de un archivo JSON que contiene tablas."""
    claims = []
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        for table_id, table_info in data.items():
            caption = table_info.get("caption", "")
            logging.debug(f"Processing table {table_id} with caption: {caption}")

            table_topic = extract_topic(caption)
            logging.debug(f"Extracted topic: {table_topic}")

            if topic_filter and table_topic != topic_filter:
                logging.debug(f"Skipping table {table_id} due to topic filter.")
                continue

            # Analizar el HTML de la tabla
            table_html = table_info.get("table", "")
            soup = BeautifulSoup(table_html, "html.parser")
            table_rows = soup.find_all("tr")

            if not table_rows:
                logging.debug(f"Table {table_id} is empty or malformed.")
                continue

            # Extraer duplas clave-valor
            key_value_pairs = extract_key_value_pairs(table_rows)

            # Generar claims usando spaCy
            dataset_name = caption.split(",")[0] if caption else "Unknown Dataset"
            formatted_claims = generate_claims_with_spacy(key_value_pairs, dataset_name, caption)

            claims.extend(formatted_claims)

    return claims

def process_json_folder(folder_path, output_folder, topic_filter=None):
    """Procesa todos los archivos JSON en una carpeta y genera un archivo de salida por cada uno."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            json_file_path = os.path.join(folder_path, file_name)
            logging.debug(f"Processing file: {json_file_path}")

            claims = extract_claims_from_table(json_file_path, topic_filter)

            # Guardar los claims extraídos en un archivo de salida
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_claims.json")
            with open(output_file_path, "w", encoding="utf-8") as f:
                json.dump(claims, f, indent=4, ensure_ascii=False)
            logging.info(f"Claims saved to {output_file_path}")

# Ejecución del script
if __name__ == "__main__":
    folder_path = r"C:\\Users\\saioa\\Desktop\\ROMA_TRE\\Ingegneria_dei_dati\\homework_4\\jsons_aproach_2"  # Cambia esta ruta
    output_folder = r"C:\\Users\\saioa\\Desktop\\ROMA_TRE\\Ingegneria_dei_dati\\homework_4\\extracted_claims_aproach_2"  # Cambia esta ruta
    topic_filter = None  # Cambiar a un tema específico si se necesita filtrar
    process_json_folder(folder_path, output_folder, topic_filter)
