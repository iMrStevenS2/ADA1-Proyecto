from datetime import date
class MaxHeap:
    def __init__(self):
        self.heap = []

    def insertar(self, tarea):
        self.heap.append(tarea)
        self._subir(len(self.heap) - 1)

    def extraer_max(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        maximo = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bajar(0)
        return maximo

    def _subir(self, idx):
        padre = (idx - 1) // 2
        if idx > 0 and self.heap[idx] > self.heap[padre]:
            self.heap[idx], self.heap[padre] = self.heap[padre], self.heap[idx]
            self._subir(padre)

    def _bajar(self, idx):
        hijo_izq = 2 * idx + 1
        hijo_der = 2 * idx + 2
        mayor = idx

        if hijo_izq < len(self.heap) and self.heap[hijo_izq] > self.heap[mayor]:
            mayor = hijo_izq
        if hijo_der < len(self.heap) and self.heap[hijo_der] > self.heap[mayor]:
            mayor = hijo_der

        if mayor != idx:
            self.heap[idx], self.heap[mayor] = self.heap[mayor], self.heap[idx]
            self._bajar(mayor)
            
    def eliminar_por_id(self, id_tarea):
        id_tarea = str(id_tarea) 
        for i, tarea in enumerate(self.heap):
            print(f"Comparando {tarea.id} con {id_tarea}")
            if str(tarea.id) == id_tarea:
                self.heap[i] = self.heap[-1]
                self.heap.pop()
                if i < len(self.heap):
                    self._subir(i)
                    self._bajar(i)
                return True
        return False

    def obtener_datos(self):
        return self.heap.copy()
    
    

