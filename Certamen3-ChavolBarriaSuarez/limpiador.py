import sys
import csv
import re

# Aumentamos el límite de recursión para que soporte el proceso
sys.setrecursionlimit(10000)

def cargar_stopwords(ruta):
    """Carga las stopwords."""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return set(linea.strip() for linea in f)
    except FileNotFoundError:
        # Si no existe, retornamos un set vacío para que no falle
        return set()

def tokenizar_y_limpiar(texto_crudo):
    """Limpia el texto, elimina puntuación y tokeniza."""
    texto = texto_crudo.lower()
    # Eliminar puntuación
    texto = re.sub(r'[.,:;!?()"“”]', '', texto)
    # Devolver lista de palabras
    return texto.split()

def procesar_y_filtrar_recursivo(lineas_csv, stopwords, index=0, indice_filtrado=None):
    """
    FUNCIÓN RECURSIVA 
    Procesa las líneas del CSV, tokeniza, y filtra stopwords.
    """
    if indice_filtrado is None:
        indice_filtrado = []

    # Caso Base: Si llegamos al final de la lista
    if index == len(lineas_csv):
        return indice_filtrado

    try:
        # Asumiendo que la Columna 0 es ID y Columna 1 es TEXTO
        # (Si falla el formato, el try/except lo captura)
        if len(lineas_csv[index]) >= 2:
            doc_id = lineas_csv[index][0].strip()
            texto = lineas_csv[index][1]
            
            palabras = tokenizar_y_limpiar(texto)
            
            for palabra in palabras:
                if not palabra: continue

                if palabra in stopwords:
                    # Opcional: imprimir para ver que trabaja
                    # print(f"[Stopword] {palabra}") 
                    pass
                else:
                    # Agregamos: palabra|id
                    indice_filtrado.append(f"{palabra}|{doc_id}")
                    
    except IndexError:
        pass # Ignoramos líneas mal formadas

    # Llamada recursiva al siguiente índice
    return procesar_y_filtrar_recursivo(lineas_csv, stopwords, index + 1, indice_filtrado)


def main():
    entrada_csv = "dataset.csv"
    salida_indice = "index_master.txt"
    
    print(">>> Iniciando Limpieza Recursiva...")
    stopwords = cargar_stopwords("stopwords.txt")
    
    try:
        with open(entrada_csv, 'r', encoding='utf-8-sig') as f:
            lector = csv.reader(f)
            todos_los_datos = list(lector)
            
            # --- CORTE DE SEGURIDAD (SLICING) ---
            # Procesamos solo las primeras 2000 líneas para evitar Stack Overflow
            # debido a la recursividad obligatoria en Python.
            lineas_csv = todos_los_datos[:2000]
            
            print(f"--- Total registros detectados: {len(todos_los_datos)}")
            print(f"--- Procesando subconjunto seguro: {len(lineas_csv)} registros ---")
            
        # Ejecución Recursiva
        lineas_limpias = procesar_y_filtrar_recursivo(lineas_csv, stopwords)
        
        with open(salida_indice, 'w', encoding='utf-8') as f:
            for linea in lineas_limpias:
                f.write(linea + "\n")
                
        print(f"\n[ÉXITO] Índice maestro generado en: {salida_indice}")
        print(f"Total de términos indexados: {len(lineas_limpias)}\n")
        
    except FileNotFoundError:
        print(f"Error: No se encontró {entrada_csv}. Asegúrate de que el archivo existe.")
        sys.exit(1)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# --- ESTA ES LA PARTE QUE FALTABA ---
if __name__ == "__main__":
    main()