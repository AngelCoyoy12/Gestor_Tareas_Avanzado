# tarea_logica.py

from datetime import datetime

class ManejadorTareas:
    def __init__(self):
        self.tareas = []
        self.tareas_completadas = []

    def agregar_tarea(self, tarea, prioridad, fecha, hora):
        nueva_tarea = {
            "tarea": tarea,
            "prioridad": prioridad,
            "fecha": fecha,
            "hora": hora,
            "completada": False
        }
        self.tareas.append(nueva_tarea)
        return self._formato_tarea(nueva_tarea)

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            return self.tareas.pop(indice)
        return None

    def obtener_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            return self._formato_tarea(self.tareas[indice])
        return None

    def modificar_tarea(self, indice, tarea, prioridad, fecha, hora):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].update({
                "tarea": tarea,
                "prioridad": prioridad,
                "fecha": fecha,
                "hora": hora
            })
            return self._formato_tarea(self.tareas[indice])
        return None

    def marcar_como_completada(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice]["completada"] = True
            tarea_completada = self.tareas.pop(indice)
            self.tareas_completadas.append(tarea_completada)
            return self._formato_tarea(tarea_completada)
        return None

    def filtrar_por_prioridad(self, prioridad):
        return [self._formato_tarea(tarea) for tarea in self.tareas if tarea["prioridad"] == prioridad]

    def obtener_todas_las_tareas(self):
        return [self._formato_tarea(tarea) for tarea in self.tareas]

    def obtener_tareas_fuera_de_tiempo(self):
        hoy = datetime.now().date()
        return [self._formato_tarea(tarea) for tarea in self.tareas 
                if datetime.strptime(tarea["fecha"], "%Y-%m-%d").date() < hoy and not tarea["completada"]]

    def obtener_tareas_completadas(self):
        return [self._formato_tarea(tarea) for tarea in self.tareas_completadas]

    def _formato_tarea(self, tarea):
        estado = "Completada" if tarea["completada"] else "Pendiente"
        return f"{tarea['tarea']} | Prioridad: {tarea['prioridad']} | Fecha: {tarea['fecha']} | Hora: {tarea['hora']} | Estado: {estado}"
