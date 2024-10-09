# tarea_logica.py

from datetime import datetime

class ManejadorTareas:
    def __init__(self):
        self.tareas = []
        self.tareas_fuera_de_tiempo = []
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

    def marcar_como_completada(self, indice, desde_fuera_tiempo=False):
        if desde_fuera_tiempo:
            if 0 <= indice < len(self.tareas_fuera_de_tiempo):
                tarea_completada = self.tareas_fuera_de_tiempo.pop(indice)
                tarea_completada["completada"] = True
                tarea_completada["fuera_de_tiempo"] = True
                self.tareas_completadas.append(tarea_completada)
                return self._formato_tarea(tarea_completada)
        else:
            if 0 <= indice < len(self.tareas):
                tarea_completada = self.tareas.pop(indice)
                tarea_completada["completada"] = True
                tarea_completada["fuera_de_tiempo"] = False
                self.tareas_completadas.append(tarea_completada)
                return self._formato_tarea(tarea_completada)
        return None
    
    def verificar_tareas_vencidas(self):
        ahora = datetime.now()
        tareas_vencidas = []
        tareas_actualizadas = []

        for tarea in self.tareas:
            fecha_hora_limite = datetime.strptime(f"{tarea['fecha']} {tarea['hora']}", "%Y-%m-%d %H:%M")
            if fecha_hora_limite < ahora and not tarea["completada"]:
                tareas_vencidas.append(tarea)
            else:
                tareas_actualizadas.append(tarea)

        self.tareas = tareas_actualizadas
        self.tareas_fuera_de_tiempo.extend(tareas_vencidas)
        return tareas_vencidas

    def filtrar_por_prioridad(self, prioridad):
        return [self._formato_tarea(tarea) for tarea in self.tareas if tarea["prioridad"] == prioridad]

    def obtener_todas_las_tareas(self):
        self.verificar_tareas_vencidas()
        return [self._formato_tarea(tarea) for tarea in self.tareas]

    def obtener_tareas_fuera_de_tiempo(self):
        return [self._formato_tarea(tarea) for tarea in self.tareas_fuera_de_tiempo]
        
    def obtener_tareas_completadas(self):
        return [self._formato_tarea(tarea) for tarea in self.tareas_completadas]

    def _formato_tarea(self, tarea):
        estado = "Completada"
        if tarea.get("completada"):
            if tarea.get("fuera_de_tiempo"):
                estado = "Completada con retraso"
        else:
            estado = "Pendiente"
        return f"{tarea['tarea']} | Prioridad: {tarea['prioridad']} | Fecha: {tarea['fecha']} | Hora: {tarea['hora']} | Estado: {estado}"

    def verificar_tareas_fuera_de_tiempo(self):
        hoy = datetime.now()
        tareas_fuera_tiempo = []

        for tarea in self.tareas:
            fecha_hora_limite = datetime.strptime(f"{tarea['fecha']} {tarea['hora']}", "%Y-%m-%d %H:%M")
            if fecha_hora_limite < hoy and not tarea["completada"]:
                tareas_fuera_tiempo.append(tarea)

        # Mueve las tareas fuera de tiempo
        for tarea in tareas_fuera_tiempo:
            self.tareas.remove(tarea)
            self.tareas_completadas.append(tarea)

        return tareas_fuera_tiempo
    
    def ordenar_por_prioridad(self):
        def prioridad_a_numero(prioridad):
            return {'Alta': 3, 'Media': 2, 'Baja': 1}.get(prioridad, 0)

        self.tareas.sort(key=lambda x: prioridad_a_numero(x['prioridad']), reverse=True)
        return [self._formato_tarea(tarea) for tarea in self.tareas]