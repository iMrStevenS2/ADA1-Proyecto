import tkinter as tk
from tkinter import ttk, messagebox

def lanzar_app():
    def agregar_tarea():
        id_tarea = entry_id.get()
        descripcion = entry_desc.get()
        prioridad = combo_prioridad.get()
        fecha = entry_fecha.get()

        if not id_tarea or not descripcion or not prioridad or not fecha:
            messagebox.showwarning("Campos incompletos", "Por favor, llena todos los campos.")
            return

        lista_tareas.insert("", "end", values=(id_tarea, descripcion, prioridad, fecha))
        limpiar_campos()

    def limpiar_campos():
        entry_id.delete(0, tk.END)
        entry_desc.delete(0, tk.END)
        combo_prioridad.set("")
        entry_fecha.delete(0, tk.END)

    def obtener_tarea_mas_prioritaria():
        prioridades = {"alta": 1, "media": 2, "baja": 3}
        tareas = lista_tareas.get_children()
        if not tareas:
            messagebox.showinfo("Sin tareas", "No hay tareas registradas.")
            return

        tarea_prioritaria = min(
            tareas,
            key=lambda t: prioridades.get(lista_tareas.item(t)["values"][2], 4)
        )
        valores = lista_tareas.item(tarea_prioritaria)["values"]
        mensaje = f"Tarea más prioritaria:\n\nID: {valores[0]}\nDesc: {valores[1]}\nPrioridad: {valores[2]}\nFecha: {valores[3]}"
        messagebox.showinfo("Más prioritaria", mensaje)

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

    tk.Label(frame_form, text="Fecha de Vencimiento:").grid(row=3, column=0, sticky="e")
    entry_fecha = tk.Entry(frame_form)
    entry_fecha.grid(row=3, column=1, padx=5)

    # Botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=5)

    tk.Button(frame_botones, text="Agregar Tarea", command=agregar_tarea).pack(side="left", padx=10)
    tk.Button(frame_botones, text="Ver Más Prioritaria", command=obtener_tarea_mas_prioritaria).pack(side="left", padx=10)

    # Tabla de tareas
    frame_lista = tk.Frame(ventana)
    frame_lista.pack(pady=10)

    columnas = ("ID", "Descripción", "Prioridad", "Fecha")
    lista_tareas = ttk.Treeview(frame_lista, columns=columnas, show="headings")

    for col in columnas:
        lista_tareas.heading(col, text=col)
        lista_tareas.column(col, width=130)

    lista_tareas.pack()

    ventana.mainloop()
