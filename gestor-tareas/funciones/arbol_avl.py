from funciones.tarea import Tarea

class NodoAVL:
    def __init__(self, tarea: Tarea):
        self.tarea = tarea
        self.izq = None
        self.der = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    # Obtener altura
    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    # Obtener factor de balance
    def _balance(self, nodo):
        return self._altura(nodo.izq) - self._altura(nodo.der) if nodo else 0

    # Rotación derecha
    def _rotar_derecha(self, y):
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        y.altura = 1 + max(self._altura(y.izq), self._altura(y.der))
        x.altura = 1 + max(self._altura(x.izq), self._altura(x.der))
        return x

    # Rotación izquierda
    def _rotar_izquierda(self, x):
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        x.altura = 1 + max(self._altura(x.izq), self._altura(x.der))
        y.altura = 1 + max(self._altura(y.izq), self._altura(y.der))
        return y

    # Insertar nodo
    def insertar(self, tarea: Tarea):
        def _insertar(nodo, tarea):
            if not nodo:
                return NodoAVL(tarea)
            if tarea.id < nodo.tarea.id:
                nodo.izq = _insertar(nodo.izq, tarea)
            elif tarea.id > nodo.tarea.id:
                nodo.der = _insertar(nodo.der, tarea)
            else:
                return nodo  # ID duplicado, no insertar

            nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
            balance = self._balance(nodo)

            # Casos de rebalanceo
            if balance > 1 and tarea.id < nodo.izq.tarea.id:
                return self._rotar_derecha(nodo)
            if balance < -1 and tarea.id > nodo.der.tarea.id:
                return self._rotar_izquierda(nodo)
            if balance > 1 and tarea.id > nodo.izq.tarea.id:
                nodo.izq = self._rotar_izquierda(nodo.izq)
                return self._rotar_derecha(nodo)
            if balance < -1 and tarea.id < nodo.der.tarea.id:
                nodo.der = self._rotar_derecha(nodo.der)
                return self._rotar_izquierda(nodo)

            return nodo

        self.raiz = _insertar(self.raiz, tarea)

    # Buscar tarea por ID
    def buscar(self, id):
        def _buscar(nodo, id):
            if not nodo:
                return None
            if id == nodo.tarea.id:
                return nodo.tarea
            elif id < nodo.tarea.id:
                return _buscar(nodo.izq, id)
            else:
                return _buscar(nodo.der, id)
        return _buscar(self.raiz, id)

    # Obtener nodo con valor mínimo
    def _minimo(self, nodo):
        actual = nodo
        while actual.izq:
            actual = actual.izq
        return actual

    # Eliminar tarea por ID
    def eliminar(self, id):
        def _eliminar(nodo, id):
            if not nodo:
                return nodo
            if id < nodo.tarea.id:
                nodo.izq = _eliminar(nodo.izq, id)
            elif id > nodo.tarea.id:
                nodo.der = _eliminar(nodo.der, id)
            else:
                if not nodo.izq:
                    return nodo.der
                elif not nodo.der:
                    return nodo.izq
                temp = self._minimo(nodo.der)
                nodo.tarea = temp.tarea
                nodo.der = _eliminar(nodo.der, temp.tarea.id)

            nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
            balance = self._balance(nodo)

            # Rebalancear
            if balance > 1 and self._balance(nodo.izq) >= 0:
                return self._rotar_derecha(nodo)
            if balance > 1 and self._balance(nodo.izq) < 0:
                nodo.izq = self._rotar_izquierda(nodo.izq)
                return self._rotar_derecha(nodo)
            if balance < -1 and self._balance(nodo.der) <= 0:
                return self._rotar_izquierda(nodo)
            if balance < -1 and self._balance(nodo.der) > 0:
                nodo.der = self._rotar_derecha(nodo.der)
                return self._rotar_izquierda(nodo)

            return nodo

        self.raiz = _eliminar(self.raiz, str(id))


    # Obtener todas las tareas en orden
    def obtener_tareas(self):
        resultado = []

        def inorden(nodo):
            if nodo:
                inorden(nodo.izq)
                resultado.append(nodo.tarea)
                inorden(nodo.der)

        inorden(self.raiz)
        return resultado

    def es_balanceado(self):
        def _verificar(nodo):
            if not nodo:
                return True, 0
            izq_ok, alt_izq = _verificar(nodo.izq)
            der_ok, alt_der = _verificar(nodo.der)

            balance = alt_izq - alt_der
            actual_ok = abs(balance) <= 1
            altura = 1 + max(alt_izq, alt_der)

            return izq_ok and der_ok and actual_ok, altura

        balanceado, _ = _verificar(self.raiz)
        return balanceado
