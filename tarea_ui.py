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
        # El código del método body permanece igual
        tk.Label(master, text="Tarea:").grid(row=0, column=0, sticky="e")
        self.e1 = tk.Entry(master, width=50)
        self.e1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Prioridad:").grid(row=1, column=0, sticky="e")
        self.prioridad = tk.StringVar(value="Media")
        tk.OptionMenu(master, self.prioridad, "Alta", "Media", "Baja").grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(master, text="Fecha límite:").grid(row=2, column=0, sticky="e")
        self.fecha_limite = DateEntry(master, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.fecha_limite.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        tk.Label(master, text="Hora límite:").grid(row=3, column=0, sticky="e")
        self.hora_limite = tk.StringVar(value="00:00")
        self.spin_hora = tk.Spinbox(master, from_=0, to=23, width=2, textvariable=self.hora_limite, format="%02.0f")
        self.spin_hora.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        tk.Label(master, text=":").grid(row=3, column=1)
        self.spin_minuto = tk.Spinbox(master, from_=0, to=59, width=2, format="%02.0f")
        self.spin_minuto.grid(row=3, column=1, sticky="w", padx=30, pady=5)

        if self.tarea:
            partes = self.tarea.split(" | ")
            self.e1.insert(0, partes[0])
            self.prioridad.set(partes[1].split(": ")[1])
            self.fecha_limite.set_date(datetime.datetime.strptime(partes[2].split(": ")[1], "%Y-%m-%d").date())
            hora = partes[3].split(": ")[1]
            self.hora_limite.set(hora.split(":")[0])
            self.spin_minuto.delete(0, tk.END)
            self.spin_minuto.insert(0, hora.split(":")[1])

        return self.e1

    def apply(self):
        tarea = self.e1.get()
        prioridad = self.prioridad.get()
        fecha = self.fecha_limite.get_date().strftime("%Y-%m-%d")
        hora = f"{self.hora_limite.get()}:{self.spin_minuto.get()}"
        self.result = (tarea, prioridad, fecha, hora)

class AplicacionListaTareas:
    def __init__(self, master):
        self.master = master
        self.master.title("Lista de Tareas Avanzada")
        self.master.geometry("700x500")
        
        self.manejador_tareas = ManejadorTareas()
        
        self.colores_prioridad = {
            "Alta": "#ffcccc",  # Rojo claro
            "Media": "#ffffcc",  # Amarillo claro
            "Baja": "#ccffcc"   # Verde claro
        }
        
        self.botones_modificables = []  # Lista para almacenar los botones que se desactivarán
        self.crear_widgets()
        self.actualizar_periodicamente()
        

    def crear_widgets(self):
        main_frame = tk.Frame(self.master, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.crear_botones_principales(main_frame)
        self.crear_pestanas(main_frame)
        self.crear_botones_secundarios(main_frame)
        
    def crear_botones_principales(self, parent):
        botones_frame = tk.Frame(parent)
        botones_frame.pack(fill=tk.X, pady=10)
        
        # Crear botones y guardarlos en la lista de botones modificables
        btn_agregar = tk.Button(botones_frame, text="Agregar Tarea", command=self.agregar_tarea, width=20)
        btn_agregar.pack(side=tk.LEFT, padx=5)
        self.botones_modificables.append(btn_agregar)
        
        btn_modificar = tk.Button(botones_frame, text="Modificar Tarea", command=self.modificar_tarea, width=20)
        btn_modificar.pack(side=tk.LEFT, padx=5)
        self.botones_modificables.append(btn_modificar)
        
        btn_completar = tk.Button(botones_frame, text="Marcar como Completada", command=self.marcar_como_completada, width=20)
        btn_completar.pack(side=tk.LEFT, padx=5)
        self.botones_modificables.append(btn_completar)
        
    def crear_pestanas(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.crear_pestana_tareas_pendientes()
        self.crear_pestana_tareas_fuera_de_tiempo()
        self.crear_pestana_tareas_completadas()
        
        # Agregar el evento de cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.actualizar_estado_botones)
        
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

    def actualizar_estado_botones(self, event=None):
        # Obtener el índice de la pestaña actual
        pestana_actual = self.notebook.select()
        indice_pestana = self.notebook.index(pestana_actual)
        
        # Habilitar/deshabilitar botones según la pestaña
        for boton in self.botones_modificables:
            if boton['text'] == "Marcar como Completada":
                # El botón de marcar como completada estará habilitado en las pestañas de pendientes y fuera de tiempo
                boton['state'] = 'normal' if indice_pestana in [0, 1] else 'disabled'
            else:
                # Los demás botones solo están habilitados en la pestaña de pendientes
                boton['state'] = 'normal' if indice_pestana == 0 else 'disabled'

    def crear_botones_secundarios(self, parent):
        botones_frame = tk.Frame(parent)
        botones_frame.pack(fill=tk.X)
        
        # Crear botón eliminar y agregarlo a la lista de botones modificables
        btn_eliminar = tk.Button(botones_frame, text="Eliminar Tarea", command=self.eliminar_tarea)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        self.botones_modificables.append(btn_eliminar)
        
        # Estos botones siempre estarán activos
        tk.Button(botones_frame, text="Ordenar por Prioridad", command=self.ordenar_por_prioridad).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Mostrar Todas", command=self.mostrar_todas).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Actualizar Listas", command=self.actualizar_todas_las_listas).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Salir", command=self.master.quit).pack(side=tk.RIGHT, padx=5)

    def obtener_prioridad_de_tarea(self, tarea_texto):
        partes = tarea_texto.split(" | ")
        for parte in partes:
            if "Prioridad:" in parte:
                return parte.split(": ")[1].strip()
        return "Media"  # Valor por defecto

    def actualizar_lista_tareas(self, listbox, tareas):
        listbox.delete(0, tk.END)
        for tarea in tareas:
            indice = listbox.size()
            listbox.insert(tk.END, tarea)
            
            # Obtener la prioridad de la tarea
            prioridad = self.obtener_prioridad_de_tarea(tarea)
            
            # Aplicar el color correspondiente
            if prioridad in self.colores_prioridad:
                listbox.itemconfig(
                    indice,
                    {'bg': self.colores_prioridad[prioridad]}
                )

    # Los demás métodos permanecen igual
    def actualizar_todas_las_listas(self):
        tareas_vencidas = self.manejador_tareas.verificar_tareas_vencidas()
        if tareas_vencidas:
            messagebox.showinfo("Tareas Vencidas", 
                f"{len(tareas_vencidas)} tarea(s) han vencido y se han movido a la pestaña de Tareas Fuera de Tiempo.")

        todas_las_tareas = self.manejador_tareas.obtener_todas_las_tareas()
        self.actualizar_lista_tareas(self.lista_tareas, todas_las_tareas)
        
        tareas_fuera_tiempo = self.manejador_tareas.obtener_tareas_fuera_de_tiempo()
        self.actualizar_lista_tareas(self.lista_tareas_fuera_tiempo, tareas_fuera_tiempo)
        
        tareas_completadas = self.manejador_tareas.obtener_tareas_completadas()
        self.actualizar_lista_tareas(self.lista_tareas_completadas, tareas_completadas)

    def agregar_tarea(self):
        dialogo = VentanaEmergente(self.master, "Agregar Nueva Tarea")
        if dialogo.result:
            tarea, prioridad, fecha, hora = dialogo.result
            if tarea:
                nueva_tarea = self.manejador_tareas.agregar_tarea(tarea, prioridad, fecha, hora)
                self.actualizar_todas_las_listas()
            else:
                messagebox.showwarning("Entrada Inválida", "Por favor llene todos los campos asignados")

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
                    tarea, prioridad, fecha, hora = dialogo.result
                    if tarea:
                        self.manejador_tareas.modificar_tarea(indice, tarea, prioridad, fecha, hora)
                        self.actualizar_todas_las_listas()
                    else:
                        messagebox.showwarning("Entrada Inválida", "Por favor, ingrese una tarea válida")
        except IndexError:
            messagebox.showwarning("Selección Vacía", "Por favor, seleccione una tarea para modificar")

    def marcar_como_completada(self):
        pestana_actual = self.notebook.index(self.notebook.select())
        try:
            if pestana_actual == 0:  # Tareas pendientes
                indice = self.lista_tareas.curselection()[0]
                if messagebox.askyesno("Confirmar", "¿Marcar esta tarea como completada?"):
                    self.manejador_tareas.marcar_como_completada(indice)
                    self.actualizar_todas_las_listas()
            elif pestana_actual == 1:  # Tareas fuera de tiempo
                indice = self.lista_tareas_fuera_tiempo.curselection()[0]
                if messagebox.askyesno("Confirmar", "¿Marcar esta tarea como completada con retraso?"):
                    if self.manejador_tareas.marcar_como_completada(indice, desde_fuera_tiempo=True):
                        self.actualizar_todas_las_listas()
                        messagebox.showinfo("Tarea Completada", "La tarea ha sido marcada como completada con retraso")
        except IndexError:
            messagebox.showwarning("Selección Vacía", "Por favor, seleccione una tarea para marcar como completada")


    def ordenar_por_prioridad(self):
        tareas_ordenadas = self.manejador_tareas.ordenar_por_prioridad()
        self.actualizar_lista_tareas(self.lista_tareas, tareas_ordenadas)
        messagebox.showinfo("Tareas Ordenadas", "Las tareas han sido ordenadas por prioridad de Alta a Baja.")

    def actualizar_periodicamente(self):
        self.actualizar_todas_las_listas()
        self.master.after(60000, self.actualizar_periodicamente)  # Actualizar cada minuto

    def mostrar_todas(self):
        self.actualizar_todas_las_listas()