from datetime import datetime, date

class Tarea:
    prioridad_valor = {"alta": 3, "media": 2, "baja": 1}
    

    def __init__(self, id, descripcion, prioridad, fecha):
        self.id = str(id)  # Asegura que siempre sea string
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.fecha = fecha

    def __lt__(self, other):
        return Tarea.prioridad_valor[self.prioridad] < Tarea.prioridad_valor[other.prioridad]

    def __gt__(self, other):
        return Tarea.prioridad_valor[self.prioridad] > Tarea.prioridad_valor[other.prioridad]

    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "fecha": self.fecha
        }

    @staticmethod
    def from_dict(data):
        if data["prioridad"] not in Tarea.prioridad_valor:
           raise ValueError(f"Prioridad inválida: {data['prioridad']}")

        return Tarea(
            data["id"],
            data["descripcion"],
            data["prioridad"],
            data["fecha"]
        )
