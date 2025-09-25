class Proceso:
    def __init__(self, id: str, tamaño: int, tiempo_arribo: int, tiempo_irrupcion: int):
        self.id = id
        self.tamaño = tamaño
        self.tiempo_arribo = tiempo_arribo
        self.tiempo_irrupcion = tiempo_irrupcion
        self.tiempo_restante = tiempo_irrupcion
        self.estado = "Nuevo"

    def __str__(self):
        return f"Proceso({self.id}, tamaño={self.tamaño}K, arribo={self.tiempo_arribo}, irrupción={self.tiempo_irrupcion})"

