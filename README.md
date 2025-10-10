# SO-Metallinux

## Descripcion
SO-Metallinux es un simulador de un sistema operativo desarrollado en Python. Este proyecto simula la gestión de procesos, la planificación de la CPU utilizando el algoritmo SRTF (Shortest Remaining Time First) y la gestión de memoria mediante el algoritmo Best-Fit.

## Caracteristicas
- **Carga de procesos desde CSV:** Los procesos a simular se cargan desde un archivo `procesos.csv`.
- **Algoritmo de planificación SRTF:** El planificador de la CPU utiliza el algoritmo SRTF para decidir qué proceso ejecutar.
- **Gestión de memoria Best-Fit:** Se implementa un gestor de memoria que utiliza el algoritmo Best-Fit para asignar particiones de memoria a los procesos.
- **Simulación de estados de procesos:** Los procesos transitan por los estados de Nuevo, Listo, Ejecución, Suspendido y Terminado.
- **Generación de estadísticas:** Al finalizar la simulación, se generan estadísticas como el tiempo de retorno promedio, el tiempo de espera promedio y el uso de la CPU.

## Como ejecutar
1.  Asegúrese de tener Python 3.x instalado.
2.  El archivo `procesos.csv` en la carpeta `data` debe contener los procesos a simular, con las columnas `id`, `tamaño`, `tiempo_arribo` y `tiempo_irrupcion`.
3.  Ejecute el siguiente comando en la raíz del proyecto:
    ```bash
    python src/main.py
    ```

## Estructura del Proyecto
```
SO-Metallinux/
├── data/
│   └── procesos.csv
├── src/
│   ├── core/
│   │   ├── colas.py
│   │   ├── cpu.py
│   │   ├── gestor_memoriaBestFit.py
│   │   ├── particion.py
│   │   ├── planificadorSRTF.py
│   │   ├── plantillas.py
│   │   ├── proceso.py
│   │   └── simulador.py
│   ├── utils/
│   │   └── archivo_reader.py
│   └── main.py
└── README.md
```
- **`data/procesos.csv`**: Archivo CSV que contiene la definición de los procesos a simular.
- **`src/core/`**: Contiene la lógica principal del simulador, incluyendo la CPU, el gestor de memoria, el planificador y las clases de proceso.
- **`src/utils/`**: Utilidades para leer y procesar el archivo de entrada.
- **`src/main.py`**: Punto de entrada de la aplicación.
