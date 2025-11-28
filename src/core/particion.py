class Particion:
    """
    Representa una partición de memoria en el sistema.
    """
    def __init__(self, id: str, direccion_inicio: int, tamaño: int):
        self.id = id
        self.direccion_inicio = direccion_inicio
        self.tamaño = tamaño
        self.proceso_asignado: Proceso | None = None
        self.fragmentacion_interna = 0
        
    
    def __str__(self):
        return f"Partición {self.id}: {self.tamaño}K, inicio: {self.direccion_inicio}"
        
    def esta_libre(self)->bool:
        return self.proceso_asignado is None