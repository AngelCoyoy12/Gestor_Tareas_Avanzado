# main.py

import tkinter as tk # Importar tk para uso de interfaz grafica
from tarea_ui import AplicacionListaTareas

def main():
    root = tk.Tk() # Crea la ventana principal
    app = AplicacionListaTareas(root)
    root.mainloop() #Mantiene la ventana activa

if __name__ == "__main__":
    main()  