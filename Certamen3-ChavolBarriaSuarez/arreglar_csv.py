import csv

entrada = "dataset.csv"
salida = "dataset_corregido.csv"

print("--- Arreglando el archivo CSV ---")
with open(entrada, 'r', encoding='utf-8') as fin, \
     open(salida, 'w', newline='', encoding='utf-8') as fout:
    
    lector = csv.reader(fin)
    escritor = csv.writer(fout)
    
    # Saltamos la cabecera original (text,label)
    next(lector, None)
    
    contador = 1
    for fila in lector:
        if len(fila) >= 1:
            texto_noticia = fila[0] # El texto está en la primera columna
            
            # Escribimos: ID, TEXTO
            escritor.writerow([contador, texto_noticia])
            contador += 1

print(f"¡Listo! Se creó '{salida}' con {contador-1} registros ordenados.")
print("Ahora renombra 'dataset_corregido.csv' a 'dataset.csv' y ejecuta el limpiador.")