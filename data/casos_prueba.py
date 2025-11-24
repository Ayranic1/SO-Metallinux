# casos_prueba_generator.py
import csv

# Caso 1: Procesos normales que caben en las particiones
def generar_caso_normal():
    procesos = [
        ['P1', 30, 0, 8],
        ['P2', 45, 1, 5],
        ['P3', 120, 2, 10],
        ['P4', 80, 3, 6],
        ['P5', 200, 4, 12],
        ['P6', 25, 5, 4],
        ['P7', 180, 6, 8],
        ['P8', 60, 7, 7],
        ['P9', 140, 8, 9],
        ['P10', 40, 9, 5]
    ]
    
    with open('caso_normal.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion'])
        writer.writerows(procesos)

# Caso 2: Procesos con tamaños límite de las particiones
def generar_caso_limites():
    procesos = [
        ['P1', 50, 0, 5],    # Exactamente la partición pequeña
        ['P2', 150, 1, 6],   # Exactamente la partición mediana
        ['P3', 250, 2, 8],   # Exactamente la partición grande
        ['P4', 49, 3, 4],    # Casi llena la pequeña
        ['P5', 149, 4, 7],   # Casi llena la mediana
        ['P6', 249, 5, 9],   # Casi llena la grande
        ['P7', 30, 6, 3],
        ['P8', 100, 7, 5],
        ['P9', 200, 8, 6],
        ['P10', 45, 9, 4]
    ]
    
    with open('caso_limites.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion'])
        writer.writerows(procesos)

# Caso 3: Procesos que exceden el tamaño máximo (250K)
def generar_caso_excedentes():
    procesos = [
        ['P1', 30, 0, 5],
        ['P2', 300, 1, 8],   # Demasiado grande - debería rechazarse
        ['P3', 120, 2, 6],
        ['P4', 400, 3, 10],  # Demasiado grande - debería rechazarse
        ['P5', 80, 4, 4],
        ['P6', 280, 5, 7],   # Demasiado grande - debería rechazarse
        ['P7', 60, 6, 3],
        ['P8', 150, 7, 5],
        ['P9', 200, 8, 6],
        ['P10', 40, 9, 4]
    ]
    
    with open('caso_excedentes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion'])
        writer.writerows(procesos)

# Caso 4: Procesos con llegadas escalonadas
def generar_caso_escalonado():
    procesos = [
        ['P1', 80, 0, 8],
        ['P2', 120, 0, 6],   # Mismo tiempo de arribo
        ['P3', 40, 5, 4],    # Llega después
        ['P4', 180, 5, 7],   # Llega después
        ['P5', 60, 10, 5],   # Llega mucho después
        ['P6', 200, 10, 9],
        ['P7', 30, 15, 3],
        ['P8', 150, 15, 6],
        ['P9', 90, 20, 4],
        ['P10', 140, 20, 7]
    ]
    
    with open('caso_escalonado.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion'])
        writer.writerows(procesos)

# Caso 5: Procesos cortos vs largos (para testear SRTF)
def generar_caso_srtf():
    procesos = [
        ['P1', 50, 0, 15],   # Largo
        ['P2', 100, 1, 3],   # Corto - debería interrumpir
        ['P3', 80, 2, 12],   # Largo
        ['P4', 120, 3, 2],   # Muy corto - debería interrumpir
        ['P5', 60, 4, 8],    # Medio
        ['P6', 150, 5, 4],   # Corto
        ['P7', 40, 6, 10],   # Largo
        ['P8', 200, 7, 1],   # Muy corto
        ['P9', 70, 8, 6],    # Medio
        ['P10', 90, 9, 3]    # Corto
    ]
    
    with open('caso_srtf.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion'])
        writer.writerows(procesos)

# Caso 6: Llenado máximo de memoria
def generar_caso_memoria_llena():
    procesos = [
        ['P1', 200, 0, 5],   # Ocupa grande
        ['P2', 140, 0, 4],   # Ocupa mediana
        ['P3', 45, 0, 3],    # Ocupa pequeña
        ['P4', 180, 1, 6],   # Espera - no hay lugar
        ['P5', 60, 2, 4],    # Espera - no hay lugar
        ['P6', 120, 3, 5],   # Espera - no hay lugar
        ['P7', 30, 10, 2],   # Llega después
        ['P8', 100, 11, 3],  # Llega después
        ['P9', 160, 12, 4],  # Llega después
        ['P10', 50, 13, 2]   # Llega después
    ]
    
    with open('caso_memoria_llena.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion'])
        writer.writerows(procesos)

# Caso 7: Fragmentación interna
def generar_caso_fragmentacion():
    procesos = [
        ['P1', 30, 0, 5],    # Pequeña: frag interna = 20
        ['P2', 100, 1, 4],   # Mediana: frag interna = 50
        ['P3', 180, 2, 6],   # Grande: frag interna = 70
        ['P4', 25, 3, 3],    # Pequeña: frag interna = 25
        ['P5', 80, 4, 5],    # Mediana: frag interna = 70
        ['P6', 220, 5, 7],   # Grande: frag interna = 30
        ['P7', 10, 6, 2],    # Pequeña: frag interna = 40
        ['P8', 120, 7, 4],   # Mediana: frag interna = 30
        ['P9', 200, 8, 6],   # Grande: frag interna = 50
        ['P10', 5, 9, 1]     # Pequeña: frag interna = 45
    ]
    
    with open('caso_fragmentacion.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion'])
        writer.writerows(procesos)

# Caso 8: Mezcla de todos los escenarios
def generar_caso_complejo():
    procesos = [
        ['P1', 250, 0, 10],  # Exacto grande
        ['P2', 50, 1, 3],    # Exacto pequeño
        ['P3', 300, 2, 5],   # Excedente - rechazado
        ['P4', 150, 3, 6],   # Exacto mediano
        ['P5', 20, 4, 2],    # Corto en pequeña
        ['P6', 180, 5, 8],   # Grande con frag
        ['P7', 100, 6, 4],   # Mediano con frag
        ['P8', 45, 7, 3],    # Pequeño con frag
        ['P9', 400, 8, 7],   # Excedente - rechazado
        ['P10', 120, 9, 5]   # Mediano con frag
    ]
    
    with open('caso_complejo.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion'])
        writer.writerows(procesos)

# Generar todos los casos de prueba
if __name__ == "__main__":
    generar_caso_normal()
    generar_caso_limites()
    generar_caso_excedentes()
    generar_caso_escalonado()
    generar_caso_srtf()
    generar_caso_memoria_llena()
    generar_caso_fragmentacion()
    generar_caso_complejo()
    
    print("Se han generado 8 archivos CSV de casos de prueba:")
    print("1. caso_normal.csv - Procesos normales")
    print("2. caso_limites.csv - Procesos con tamaños límite")
    print("3. caso_excedentes.csv - Procesos que exceden 250K")
    print("4. caso_escalonado.csv - Llegadas escalonadas")
    print("5. caso_srtf.csv - Para testear algoritmo SRTF")
    print("6. caso_memoria_llena.csv - Para testear suspensión")
    print("7. caso_fragmentacion.csv - Para analizar fragmentación interna")
    print("8. caso_complejo.csv - Mezcla de todos los escenarios")