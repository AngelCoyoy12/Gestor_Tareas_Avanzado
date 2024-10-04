# tarea_ui.py

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import DateEntry
import datetime
from tarea_logica import ManejadorTareas

class VentanaEmergente(simpledialog.Dialog):
    def __init__(self, parent, title, tarea=None):
        self.tarea = tarea
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Tarea:").grid(row=0, column=0, sticky="e")
        self.e1 = tk.Entry(master, width=50)
        self.e1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Prioridad:").grid(row=1, column=0, sticky="e")
        self.prioridad = tk.StringVar(value="Media")
        tk.OptionMenu(master, self.prioridad, "Alta", "Media", "Baja").grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(master, text="Fecha límite:").grid(row=2, column=0, sticky="e")
        self.fecha_limite = DateEntry(master, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.fecha_limite.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        if self.tarea:
            partes = self.tarea.split(" | ")
            self.e1.insert(0, partes[0])
            self.prioridad.set(partes[1].split(": ")[1])
            self.fecha_limite.set_date(datetime.datetime.strptime(partes[2].split(": ")[1], "%Y-%m-%d").date())

        return self.e1  # initial focus

    def apply(self):
        tarea = self.e1.get()
        prioridad = self.prioridad.get()
        fecha = self.fecha_limite.get_date().strftime("%Y-%m-%d")
        self.result = (tarea, prioridad, fecha)

class AplicacionListaTareas:
    def __init__(self, master):
        self.master = master
        self.master.title("Lista de Tareas Avanzada")
        self.master.geometry("700x500")
        
        self.manejador_tareas = ManejadorTareas()
        
        self.crear_widgets()
        
    def crear_widgets(self):
        main_frame = tk.Frame(self.master, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.crear_botones_principales(main_frame)
        self.crear_pestanas(main_frame)
        self.crear_botones_secundarios(main_frame)
        
    def crear_botones_principales(self, parent):
        botones_frame = tk.Frame(parent)
        botones_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(botones_frame, text="Agregar Tarea", command=self.agregar_tarea, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Modificar Tarea", command=self.modificar_tarea, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Marcar como Completada", command=self.marcar_como_completada, width=20).pack(side=tk.LEFT, padx=5)
        
    def crear_pestanas(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.crear_pestana_tareas_pendientes()
        self.crear_pestana_tareas_fuera_de_tiempo()
        self.crear_pestana_tareas_completadas()
        
    def crear_pestana_tareas_pendientes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tareas Pendientes")
        
        self.lista_tareas = tk.Listbox(frame, height=15, width=80)
        self.lista_tareas.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def crear_pestana_tareas_fuera_de_tiempo(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tareas Fuera de Tiempo")
        
        self.lista_tareas_fuera_tiempo = tk.Listbox(frame, height=15, width=80)
        self.lista_tareas_fuera_tiempo.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def crear_pestana_tareas_completadas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tareas Completadas")
        
        self.lista_tareas_completadas = tk.Listbox(frame, height=15, width=80)
        self.lista_tareas_completadas.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def crear_botones_secundarios(self, parent):
        botones_frame = tk.Frame(parent)
        botones_frame.pack(fill=tk.X)
        
        tk.Button(botones_frame, text="Eliminar Tarea", command=self.eliminar_tarea).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Filtrar por Prioridad", command=self.filtrar_por_prioridad).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Mostrar Todas", command=self.mostrar_todas).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Actualizar Listas", command=self.actualizar_todas_las_listas).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Salir", command=self.master.quit).pack(side=tk.RIGHT, padx=5)
        
    def agregar_tarea(self):
        dialogo = VentanaEmergente(self.master, "Agregar Nueva Tarea")
        if dialogo.result:
            tarea, prioridad, fecha = dialogo.result
            if tarea:
                nueva_tarea = self.manejador_tareas.agregar_tarea(tarea, prioridad, fecha)
                self.lista_tareas.insert(tk.END, nueva_tarea)
                self.actualizar_todas_las_listas()
            else:
                messagebox.showwarning("Entrada Inválida", "Por favor, ingrese una tarea válida")
    
    def eliminar_tarea(self):
        try:
            indice = self.lista_tareas.curselection()[0]
            if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar esta tarea?"):
                self.manejador_tareas.eliminar_tarea(indice)
                self.actualizar_todas_las_listas()
        except IndexError:
            messagebox.showwarning("Selección Vacía", "Por favor, seleccione una tarea para eliminar")
    
    def modificar_tarea(self):
        try:
            indice = self.lista_tareas.curselection()[0]
            tarea_actual = self.manejador_tareas.obtener_tarea(indice)
            if tarea_actual:
                dialogo = VentanaEmergente(self.master, "Modificar Tarea", tarea_actual)
                if dialogo.result:
                    tarea, prioridad, fecha = dialogo.result
                    if tarea:
                        self.manejador_tareas.modificar_tarea(indice, tarea, prioridad, fecha)
                        self.actualizar_todas_las_listas()
                    else:
                        messagebox.showwarning("Entrada Inválida", "Por favor, ingrese una tarea válida")
        except IndexError:
            messagebox.showwarning("Selección Vacía", "Por favor, seleccione una tarea para modificar")
    
    def marcar_como_completada(self):
        try:
            indice = self.lista_tareas.curselection()[0]
            if messagebox.askyesno("Confirmar", "¿Marcar esta tarea como completada?"):
                self.manejador_tareas.marcar_como_completada(indice)
                self.actualizar_todas_las_listas()
        except IndexError:
            messagebox.showwarning("Selección Vacía", "Por favor, seleccione una tarea para marcar como completada")
    
    def filtrar_por_prioridad(self):
        prioridad = simpledialog.askstring("Filtrar por Prioridad", "Ingrese la prioridad (Alta, Media, Baja):")
        if prioridad:
            tareas_filtradas = self.manejador_tareas.filtrar_por_prioridad(prioridad)
            self.actualizar_lista_tareas(self.lista_tareas, tareas_filtradas)
    
    def mostrar_todas(self):
        self.actualizar_todas_las_listas()
    
    def actualizar_lista_tareas(self, listbox, tareas):
        listbox.delete(0, tk.END)
        for tarea in tareas:
            listbox.insert(tk.END, tarea)
    
    def actualizar_todas_las_listas(self):
        todas_las_tareas = self.manejador_tareas.obtener_todas_las_tareas()
        self.actualizar_lista_tareas(self.lista_tareas, todas_las_tareas)
        
        tareas_fuera_tiempo = self.manejador_tareas.obtener_tareas_fuera_de_tiempo()
        self.actualizar_lista_tareas(self.lista_tareas_fuera_tiempo, tareas_fuera_tiempo)
        
        tareas_completadas = self.manejador_tareas.obtener_tareas_completadas()
        self.actualizar_lista_tareas(self.lista_tareas_completadas, tareas_completadas)