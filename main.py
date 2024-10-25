# main.py

import tkinter as tk  # Importa el módulo tkinter para crear interfaces gráficas.
from tarea_ui import AplicacionListaTareas  # Importa  AplicacionListaTareas.

def main():
    root = tk.Tk()  # Crea la ventana principal .
    root.resizable(False, False)  # NO redimensionar.
    app = AplicacionListaTareas(root)  # Crea una instancia de la aplicación de lista de tareas.
    root.mainloop()  # Inicia el bucle principal de la aplicación.

if __name__ == "__main__":
    main()  # Si el script se ejecuta directamente inicia la aplicación.
