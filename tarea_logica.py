# tarea_logica.py
import babel.numbers
from datetime import datetime, timedelta
from notifypy import Notify
import threading
import time

class ManejadorTareas:
    def __init__(self):
        self.tareas = []
        self.tareas_fuera_de_tiempo = []
        self.tareas_completadas = []
        self.notificaciones_enviadas = {}  # Para rastrear notificaciones enviadas
        # Iniciar el hilo de verificación de notificaciones
        self.iniciar_verificador_notificaciones()

    def crear_notificacion(self, titulo, mensaje):
        # Crea y muestra una notificación del sistema
        notificacion = Notify()
        notificacion.title = titulo
        notificacion.message = mensaje
        notificacion.icon = "1497619898-jd24_85173.ico"  # Puedes personalizar el ícono
        try:
            notificacion.send()
        except Exception as e:
            print(f"Error al enviar notificación: {e}")

    def verificar_proximidad_vencimiento(self, tarea):
        # Verifica si una tarea está próxima a vencer y envía notificaciones apropiadas
        if tarea["completada"]:
            return

        # Obtener la fecha y hora actual
        ahora = datetime.now()
        fecha_hora_limite = datetime.strptime(f"{tarea['fecha']} {tarea['hora']}", "%Y-%m-%d %H:%M")
        
        # Calcular la diferencia de tiempo
        tiempo_restante = fecha_hora_limite - ahora
        minutos_restantes = tiempo_restante.total_seconds() / 60

        # Identificador único para la tarea
        tarea_id = f"{tarea['tarea']}_{tarea['fecha']}_{tarea['hora']}"
        
        # Verificar diferentes umbrales de tiempo y enviar notificaciones
        if tiempo_restante.total_seconds() < 0:  # Tarea vencida
            if self.notificaciones_enviadas.get(tarea_id, {}).get('vencida') != True:
                self.crear_notificacion(
                    "Mala suerta",
                    f"La tarea '{tarea['tarea']}' ha vencido."
                )
                self.notificaciones_enviadas.setdefault(tarea_id, {})['vencida'] = True

        elif 0 <= minutos_restantes <= 30:  # 30 minutos o menos
            if self.notificaciones_enviadas.get(tarea_id, {}).get('30min') != True:
                self.crear_notificacion(
                    "Advertencia de Tarea",
                    f"La tarea '{tarea['tarea']}' vence en menos de 30 minutos."
                )
                self.notificaciones_enviadas.setdefault(tarea_id, {})['30min'] = True

        elif 30 < minutos_restantes <= 60:  # Entre 30 y 60 minutos
            if self.notificaciones_enviadas.get(tarea_id, {}).get('1hora') != True:
                self.crear_notificacion(
                    "Recordatorio de Tarea",
                    f"La tarea '{tarea['tarea']}' vence en 1 hora."
                )
                self.notificaciones_enviadas.setdefault(tarea_id, {})['1hora'] = True

    def verificar_todas_las_tareas(self):
        # Verifica todas las tareas pendientes para notificaciones
        for tarea in self.tareas:
            self.verificar_proximidad_vencimiento(tarea)

    def iniciar_verificador_notificaciones(self):
        # Inicia un hilo para verificar periódicamente las notificaciones
        def verificador():
            while True:
                self.verificar_todas_las_tareas()
                time.sleep(60)  # Verificar cada minuto

        # Crear y iniciar el hilo
        hilo_verificador = threading.Thread(target=verificador, daemon=True)
        hilo_verificador.start()

    def agregar_tarea(self, tarea, prioridad, fecha, hora):
        nueva_tarea = {
            "tarea": tarea,
            "prioridad": prioridad,
            "fecha": fecha,
            "hora": hora,
            "completada": False
        }
        self.tareas.append(nueva_tarea)
        
        # Verificar inmediatamente la proximidad al vencimiento
        self.verificar_proximidad_vencimiento(nueva_tarea)
        
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
            # Verificar proximidad al vencimiento después de la modificación
            self.verificar_proximidad_vencimiento(self.tareas[indice])
            return self._formato_tarea(self.tareas[indice])
        return None

    def marcar_como_completada(self, indice, desde_fuera_tiempo=False):
        if desde_fuera_tiempo:
            if 0 <= indice < len(self.tareas_fuera_de_tiempo):
                tarea_completada = self.tareas_fuera_de_tiempo.pop(indice)
                tarea_completada["completada"] = True
                tarea_completada["fuera_de_tiempo"] = True  # Marcador para tareas completadas con retraso
                self.tareas_completadas.append(tarea_completada)
                return self._formato_tarea(tarea_completada)
        else:
            if 0 <= indice < len(self.tareas):
                tarea_completada = self.tareas.pop(indice)
                tarea_completada["completada"] = True
                tarea_completada["fuera_de_tiempo"] = False  # Marcador para tareas completadas a tiempo
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
                # Enviar notificación de vencimiento si no se ha enviado antes
                tarea_id = f"{tarea['tarea']}_{tarea['fecha']}_{tarea['hora']}"
                if not self.notificaciones_enviadas.get(tarea_id, {}).get('vencida'):
                    self.crear_notificacion(
                        "Tarea Vencida",
                        f"La tarea '{tarea['tarea']}' ha sido movida a tareas vencidas."
                    )
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
        estado = "Completada"
        if tarea.get("completada"):
            if tarea.get("fuera_de_tiempo"):
                estado = "Completada con retraso"
        else:
            estado = "Pendiente"
        return f"{tarea['tarea']} | Prioridad: {tarea['prioridad']} | Fecha: {tarea['fecha']} | Hora: {tarea['hora']} | Estado: {estado}"

    def ordenar_por_prioridad(self):
        def prioridad_a_numero(prioridad):
            return {'Alta': 3, 'Media': 2, 'Baja': 1}.get(prioridad, 0)

        self.tareas.sort(key=lambda x: prioridad_a_numero(x['prioridad']), reverse=True)
        return [self._formato_tarea(tarea) for tarea in self.tareas]

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
            self.tareas_fuera_de_tiempo.append(tarea)

        return tareas_fuera_tiempo

    