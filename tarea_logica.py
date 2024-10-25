#tarealogica.py

import json  # Manejo de archivos JSON.
import os  # Interacción con el sistema operativo.
from datetime import datetime  # Manejo de fechas y horas.
from notifypy import Notify  # Envío de notificaciones.
import threading  # Manejo de hilos.
import time  # Funciones relacionadas con el tiempo.


class ManejadorTareas:
    def __init__(self):
        self.tareas = []
        self.tareas_fuera_de_tiempo = []
        self.tareas_completadas = []
        self.notificaciones_enviadas = {}
        self.cargar_tareas()
        self.iniciar_verificador_notificaciones()

    def crear_notificacion(self, titulo, mensaje):
        notificacion = Notify()
        notificacion.title = titulo
        notificacion.message = mensaje
        notificacion.icon = "1497619898-jd24_85173.ico"
        try:
            notificacion.send()
        except Exception as e:
            print(f"Error al enviar notificación: {e}")

    def verificar_proximidad_vencimiento(self, tarea):
        if tarea["completada"]:
            return

        ahora = datetime.now()
        fecha_hora_limite = datetime.strptime(f"{tarea['fecha']} {tarea['hora']}", "%Y-%m-%d %H:%M")
        tiempo_restante = fecha_hora_limite - ahora
        minutos_restantes = tiempo_restante.total_seconds() / 60
        tarea_id = f"{tarea['tarea']}_{tarea['fecha']}_{tarea['hora']}"

        if tiempo_restante.total_seconds() < 0:
            if self.notificaciones_enviadas.get(tarea_id, {}).get('vencida') != True:
                self.crear_notificacion("Mala suerte", f"La tarea '{tarea['tarea']}' ha vencido.")
                self.notificaciones_enviadas.setdefault(tarea_id, {})['vencida'] = True
        elif 0 <= minutos_restantes <= 30:
            if self.notificaciones_enviadas.get(tarea_id, {}).get('30min') != True:
                self.crear_notificacion("Advertencia de Tarea", f"La tarea '{tarea['tarea']}' vence en menos de 30 minutos.")
                self.notificaciones_enviadas.setdefault(tarea_id, {})['30min'] = True
        elif 30 < minutos_restantes <= 60:
            if self.notificaciones_enviadas.get(tarea_id, {}).get('1hora') != True:
                self.crear_notificacion("Recordatorio de Tarea", f"La tarea '{tarea['tarea']}' vence en 1 hora.")
                self.notificaciones_enviadas.setdefault(tarea_id, {})['1hora'] = True

    def verificar_todas_las_tareas(self):
        for tarea in self.tareas:
            self.verificar_proximidad_vencimiento(tarea)

    def iniciar_verificador_notificaciones(self):
        def verificador():
            while True:
                self.verificar_todas_las_tareas()
                time.sleep(60)

        hilo_verificador = threading.Thread(target=verificador, daemon=True)
        hilo_verificador.start()

    def guardar_tareas(self):
        data = {
            "tareas": self.tareas,
            "tareas_fuera_de_tiempo": self.tareas_fuera_de_tiempo,
            "tareas_completadas": self.tareas_completadas
        }
        with open('tareas.json', 'w') as file:
            json.dump(data, file)

    def cargar_tareas(self):
        if os.path.exists('tareas.json'):
            with open('tareas.json', 'r') as file:
                try:
                    data = json.load(file)
                    if isinstance(data, dict):
                        self.tareas = data.get("tareas", [])
                        self.tareas_fuera_de_tiempo = data.get("tareas_fuera_de_tiempo", [])
                        self.tareas_completadas = data.get("tareas_completadas", [])
                    else:
                        print("Formato de archivo incorrecto. Se inicializarán listas vacías.")
                        self.tareas = []
                        self.tareas_fuera_de_tiempo = []
                        self.tareas_completadas = []
                except json.JSONDecodeError:
                    print("Error JSON.")
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
        self.guardar_tareas()
        self.verificar_proximidad_vencimiento(nueva_tarea)
        return self._formato_tarea(nueva_tarea)

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            tarea_eliminada = self.tareas.pop(indice)
            self.guardar_tareas()
            return tarea_eliminada
        return None

    def eliminar_tarea_completada(self, indice):
        if 0 <= indice < len(self.tareas_completadas):
            self.tareas_completadas.pop(indice)
            self.guardar_tareas()
            return True
        return False

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
            self.verificar_proximidad_vencimiento(self.tareas[indice])
            self.guardar_tareas()
            return self._formato_tarea(self.tareas[indice])
        return None

    def marcar_como_completada(self, indice, desde_fuera_tiempo=False):
        if desde_fuera_tiempo:
            if 0 <= indice < len(self.tareas_fuera_de_tiempo):
                tarea_completada = self.tareas_fuera_de_tiempo.pop(indice)
                tarea_completada["completada"] = True
                tarea_completada["fuera_de_tiempo"] = True
                self.tareas_completadas.append(tarea_completada)
                self.guardar_tareas()
                return self._formato_tarea(tarea_completada)
        else:
            if 0 <= indice < len(self.tareas):
                tarea_completada = self.tareas.pop(indice)
                tarea_completada["completada"] = True
                tarea_completada["fuera_de_tiempo"] = False
                self.tareas_completadas.append(tarea_completada)
                self.guardar_tareas()
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
                tarea_id = f"{tarea['tarea']}_{tarea['fecha']}_{tarea['hora']}"
                if not self.notificaciones_enviadas.get(tarea_id, {}).get('vencida'):
                    self.crear_notificacion("Tarea Vencida", f"La tarea '{tarea['tarea']}' ha sido movida a tareas vencidas.")
                    self.notificaciones_enviadas.setdefault(tarea_id, {})['vencida'] = True
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
        estado = "Completada" if tarea.get("completada") else "Pendiente"
        if tarea.get("fuera_de_tiempo"):
            estado = "Completada con retraso"
        return f"{tarea['tarea']} | Prioridad: {tarea['prioridad']} | Fecha: {tarea['fecha']} | Hora: {tarea['hora']} | Estado: {estado}"

    def ordenar_por_prioridad(self):
        def prioridad_a_numero(prioridad):
            return {'Alta': 3, 'Media': 2, 'Baja': 1}.get(prioridad, 0)

        self.tareas.sort(key=lambda x: prioridad_a_numero(x['prioridad']), reverse=True)
        return [self._formato_tarea(tarea) for tarea in self.tareas]
