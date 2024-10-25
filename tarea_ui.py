#tarea_ui
import tkinter as tk #interfaz grafica
from tkinter import messagebox, simpledialog, ttk #mensajes texto, widgets y dialogos
from tkcalendar import DateEntry
import datetime
from tarea_logica import ManejadorTareas
from PIL import Image, ImageTk #imagenes a formato tk

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

        self.configurar_fondo()

        
        self.colores_prioridad = {
            "Alta": "#ffcccc",
            "Media": "#ffffcc",
            "Baja": "#ccffcc"
        }
        
        # Configurar el estilo para las pestañas transparentes
        self.style = ttk.Style()
        self.style.configure('Transparent.TFrame', background='transparent')
        
        # Cargar y configurar la imagen de fondo
        try:
            # Cargar la imagen
            imagen = Image.open("imagen_2024-10-09_083216617-removebg-preview.png")  # Asegúrate de tener tu imagen en el directorio
            
            # Redimensionar la imagen al tamaño de la ventana
            imagen = imagen.resize((700, 500), Image.LANCZOS)
            
            # Convertir la imagen para tkinter
            self.imagen_fondo = ImageTk.PhotoImage(imagen)
            
            # Crear un label con la imagen de fondo
            self.fondo_label = tk.Label(self.master, image=self.imagen_fondo)
            self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
        
        self.botones_modificables = []
        self.crear_widgets()
        self.actualizar_periodicamente()
        
    def configurar_fondo(self):
        try:
            # Cargar y redimensionar la imagen de fondo
            imagen = Image.open("imagen_2024-10-09_083216617-removebg-preview.png")  # Ajusta la ruta según tu imagen
            
            # Obtener dimensiones de la ventana
            ancho_ventana = self.master.winfo_screenwidth()
            alto_ventana = self.master.winfo_screenheight()
            
            # Redimensionar la imagen
            imagen_redimensionada = imagen.resize((ancho_ventana, alto_ventana))
            
            # Convertir la imagen para Tkinter
            self.imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)
            
            # Crear label para el fondo
            self.fondo_label = tk.Label(self.master, image=self.imagen_fondo)
            self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Poner el fondo detrás de todo
            self.fondo_label.lower()
            
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            self.master.configure(bg='#f0f0f0')

    def crear_widgets(self):
    # Crear frame principal con fondo semi-transparente
        self.main_frame = tk.Frame(self.master, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar transparencia del frame principal
        self.main_frame.configure(bg='white')
        
        self.crear_botones_principales(self.main_frame)
        self.crear_pestanas(self.main_frame)
        self.crear_botones_secundarios(self.main_frame)
        
    def crear_botones_principales(self, parent):
        botones_frame = tk.Frame(parent)
        botones_frame.pack(fill=tk.X, pady=10)
        
        # Estilo para los botones
        estilo_boton = {
            'bg': '#4a90e2',
            'fg': 'white',
            'relief': tk.RAISED
        }
        
        btn_agregar = tk.Button(botones_frame, text="Agregar Tarea", 
                            command=self.agregar_tarea, width=20, **estilo_boton)
        btn_agregar.pack(side=tk.LEFT, padx=5)
        self.botones_modificables.append(btn_agregar)
        
        btn_modificar = tk.Button(botones_frame, text="Modificar Tarea", 
                                command=self.modificar_tarea, width=20, **estilo_boton)
        btn_modificar.pack(side=tk.LEFT, padx=5)
        self.botones_modificables.append(btn_modificar)
        
        btn_completar = tk.Button(botones_frame, text="Marcar como Completada", 
                                command=self.marcar_como_completada, width=20, **estilo_boton)
        btn_completar.pack(side=tk.LEFT, padx=5)
        self.botones_modificables.append(btn_completar)
            
    def crear_pestanas(self, parent):
        # Configurar estilo de las pestañas
        style = ttk.Style()
        style.configure('Custom.TNotebook', background='white')
        style.configure('Custom.TNotebook.Tab', padding=[12, 4], 
                    font=('Arial', 10))
        
        self.notebook = ttk.Notebook(parent, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.crear_pestana_tareas_pendientes()
        self.crear_pestana_tareas_fuera_de_tiempo()
        self.crear_pestana_tareas_completadas()
        
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
        pestana_actual = self.notebook.select()
        indice_pestana = self.notebook.index(pestana_actual)
        
        for boton in self.botones_modificables:
            if boton['text'] == "Marcar como Completada":
                boton['state'] = 'normal' if indice_pestana in [0, 1] else 'disabled'
            elif boton['text'] == "Eliminar Tarea":
                boton['state'] = 'normal' if indice_pestana in [0, 2] else 'disabled'
            else:
                boton['state'] = 'normal' if indice_pestana == 0 else 'disabled'

    def crear_botones_secundarios(self, parent):
        botones_frame = tk.Frame(parent)
        botones_frame.pack(fill=tk.X)
        
        btn_eliminar = tk.Button(botones_frame, text="Eliminar Tarea", command=self.eliminar_tarea)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        self.botones_modificables.append(btn_eliminar)
        
        tk.Button(botones_frame, text="Ordenar por Prioridad", command=self.ordenar_por_prioridad).pack(side=tk.LEFT, padx=5)
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
            
            prioridad = self.obtener_prioridad_de_tarea(tarea)
            
            if prioridad in self.colores_prioridad:
                listbox.itemconfig(
                    indice,
                    {'bg': self.colores_prioridad[prioridad]}
                )

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
        pestana_actual = self.notebook.index(self.notebook.select())
        try:
            if pestana_actual == 0:  # Tareas pendientes
                indice = self.lista_tareas.curselection()[0]
                if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar esta tarea?"):
                    self.manejador_tareas.eliminar_tarea(indice)
                    self.actualizar_todas_las_listas()
            elif pestana_actual == 2:  # Tareas completadas
                indice = self.lista_tareas_completadas.curselection()[0]
                if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar esta tarea completada?"):
                    if self.manejador_tareas.eliminar_tarea_completada(indice):
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
        except IndexError:
            messagebox.showwarning("Selección Vacía", "Por favor, seleccione una tarea para marcar como completada")

    def ordenar_por_prioridad(self):
        tareas_ordenadas = self.manejador_tareas.ordenar_por_prioridad()
        self.actualizar_lista_tareas(self.lista_tareas, tareas_ordenadas)

    def actualizar_periodicamente(self):
        self.actualizar_todas_las_listas()
        self.master.after(60000, self.actualizar_periodicamente)  # Actualizar cada minuto

    def mostrar_todas(self):
        self.actualizar_todas_las_listas()