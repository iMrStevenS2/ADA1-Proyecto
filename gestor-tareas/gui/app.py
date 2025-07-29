import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import date

## Importar funciones
from funciones.tarea import Tarea
from funciones.heap import MaxHeap
from funciones.arbol_avl import ArbolAVL
from funciones.archivo import cargar_tareas, guardar_tareas
import os

def mostrar_heap(heap_list):
    print("\n📦 Estado del MaxHeap:")
    for i, tarea in enumerate(heap_list):
        print(f"[{i}] ID: {tarea.id}, Prioridad: {tarea.prioridad}, Desc: {tarea.descripcion}, Fecha: {tarea.fecha}")


## Crear directorios si no existen
def crear_directorios():
    if not os.path.exists("../data"):
        os.makedirs("../data")
        
## Lanzar la aplicación y
## Cargar tareas desde archivos

def lanzar_app():
    crear_directorios()
    ruta_heap = "../data/heap_data.json"
    ruta_avl = "../data/avl_data.json"
    
    heap = MaxHeap()
    avl = ArbolAVL()
    tareas_heap = cargar_tareas(ruta_heap)
    tareas_avl = cargar_tareas(ruta_avl)

    for tarea in tareas_heap:
        heap.insertar(tarea)
        
    for tarea in tareas_avl:
        avl.insertar(tarea)

    def agregar_tarea():
        id_tarea = entry_id.get()
        descripcion = entry_desc.get()
        prioridad = combo_prioridad.get()
        fecha = entry_fecha.get()

        if not id_tarea or not descripcion or not prioridad or not fecha:
            messagebox.showwarning("Campos incompletos", "Por favor, llena todos los campos.")
            return

        if avl.buscar(id_tarea):
            messagebox.showerror("ID duplicado", "Ya existe una tarea con ese ID.")
            return

        tarea = Tarea(id_tarea, descripcion, prioridad, fecha)

        heap.insertar(tarea)
        mostrar_heap(heap.heap)
        avl.insertar(tarea)

        print("ruta_heap:", ruta_heap, type(ruta_heap))

        guardar_tareas(heap.obtener_datos(), ruta_heap)
        guardar_tareas(avl.obtener_tareas(), ruta_avl)

        print("¿AVL balanceado?", avl.es_balanceado())

        lista_tareas.insert("", "end", values=(id_tarea, descripcion, prioridad, fecha))
        limpiar_campos()

    def limpiar_campos():
        entry_id.delete(0, tk.END)
        entry_desc.delete(0, tk.END)
        combo_prioridad.set("")
        entry_fecha.delete(0, tk.END)

    def obtener_tarea_mas_prioritaria():
        if not heap.heap:
            messagebox.showinfo("Sin tareas", "No hay tareas registradas.")
            return

        tarea = heap.heap[0]
        mensaje = f"Tarea más prioritaria:\n\nID: {tarea.id}\nDesc: {tarea.descripcion}\nPrioridad: {tarea.prioridad}\nFecha: {tarea.fecha}"
        messagebox.showinfo("Más prioritaria", mensaje)
        

    def eliminar_tarea():
        seleccion = lista_tareas.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona una tarea", "Debes seleccionar una tarea para eliminar.")
            return

        item = lista_tareas.item(seleccion[0])
        id_tarea = item["values"][0]

        heap.eliminar_por_id(id_tarea)
        avl.eliminar(id_tarea)

        guardar_tareas(heap.obtener_datos(), ruta_heap)
        guardar_tareas(avl.obtener_tareas(), ruta_avl)

        print("¿AVL balanceado?", avl.es_balanceado())
        lista_tareas.delete(seleccion[0])

    # Ventana principal
    ventana = tk.Tk()
    ventana.title("Gestor de Tareas")
    ventana.geometry("600x400")
    ventana.resizable(False, False)

    # Formulario
    frame_form = tk.Frame(ventana)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e")
    entry_id = tk.Entry(frame_form)
    entry_id.grid(row=0, column=1, padx=5)

    tk.Label(frame_form, text="Descripción:").grid(row=1, column=0, sticky="e")
    entry_desc = tk.Entry(frame_form, width=40)
    entry_desc.grid(row=1, column=1, padx=5)

    tk.Label(frame_form, text="Prioridad:").grid(row=2, column=0, sticky="e")
    combo_prioridad = ttk.Combobox(frame_form, values=["alta", "media", "baja"], state="readonly")
    combo_prioridad.grid(row=2, column=1, padx=5)

    ### Calendario
    entry_fecha_var = tk.StringVar()

    def abrir_calendario():
        top = tk.Toplevel(ventana)
        top.grab_set()  # Modal

        cal = Calendar(top, selectmode="day",
                    year=date.today().year,
                    month=date.today().month,
                    day=date.today().day,
                    mindate=date(2020, 1, 1),
                    maxdate=date(2100, 12, 31),
                    date_pattern='yyyy-mm-dd')
        cal.pack(padx=10, pady=10)

        def seleccionar_fecha():
            entry_fecha_var.set(cal.get_date())
            top.destroy()

        tk.Button(top, text="Seleccionar", command=seleccionar_fecha).pack(pady=5)

    # Etiqueta y campo de texto con botón para abrir calendario
    tk.Label(frame_form, text="Fecha de Vencimiento:").grid(row=3, column=0, sticky="e")

    frame_fecha = tk.Frame(frame_form)
    frame_fecha.grid(row=3, column=1, padx=5)

    entry_fecha = tk.Entry(frame_fecha, textvariable=entry_fecha_var, width=16, state="readonly")
    entry_fecha.pack(side="left")

    btn_calendario = tk.Button(frame_fecha, text="📅", command=abrir_calendario)
    btn_calendario.pack(side="left", padx=2)

    ###
    # Botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=5)

    frame_busqueda = tk.Frame(ventana)
    frame_busqueda.pack(pady=5)


    tk.Button(frame_botones, text="Agregar Tarea", command=agregar_tarea).pack(side="left", padx=10)
    tk.Button(frame_botones, text="Ver Más Prioritaria", command=obtener_tarea_mas_prioritaria).pack(side="left", padx=10)
    tk.Button(frame_botones, text="Completar Tarea", command=eliminar_tarea).pack(side="left", padx=10)
    
    tk.Label(frame_busqueda, text="Buscar ID:").pack(side="left")
    entry_buscar = tk.Entry(frame_busqueda, width=15)
    entry_buscar.pack(side="left", padx=5)

    def buscar_tarea():
        id_buscado = entry_buscar.get().strip()
        if not id_buscado:
            messagebox.showwarning("Campo vacío", "Ingresa un ID para buscar.")
            return
        tarea = avl.buscar(id_buscado)
        if tarea:
            mensaje = f"Tarea encontrada:\n\nID: {tarea.id}\nDesc: {tarea.descripcion}\nPrioridad: {tarea.prioridad}\nFecha: {tarea.fecha}"
            messagebox.showinfo("Resultado", mensaje)
        else:
            messagebox.showinfo("No encontrada", f"No se encontró ninguna tarea con ID {id_buscado}.")

    tk.Button(frame_busqueda, text="Buscar", command=buscar_tarea).pack(side="left", padx=5)

    # Tabla de tareas
    frame_lista = tk.Frame(ventana)
    frame_lista.pack(pady=10)

    columnas = ("ID", "Descripción", "Prioridad", "Fecha")
    lista_tareas = ttk.Treeview(frame_lista, columns=columnas, show="headings")

    for col in columnas:
        lista_tareas.heading(col, text=col)
        lista_tareas.column(col, width=130)

    lista_tareas.pack()
    
    for tarea in heap.heap:
        lista_tareas.insert("", "end", values=(tarea.id, tarea.descripcion, tarea.prioridad, tarea.fecha))

    ventana.mainloop()
