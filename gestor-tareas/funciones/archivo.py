import json
import os
from funciones.tarea import Tarea

def guardar_tareas(lista_tareas, ruta):
    print(f"Ruta: {ruta} ({type(ruta)})")
    print(f"Tareas: {lista_tareas}")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump([tarea.to_dict() for tarea in lista_tareas], f, indent=4)
        
        
def cargar_tareas(ruta):
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        try:
            datos = json.load(f)
            return [Tarea.from_dict(d) for d in datos]
        except json.JSONDecodeError:
            return []

