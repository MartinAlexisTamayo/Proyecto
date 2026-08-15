"""
processor.py
Módulo que contiene la lógica de procesamiento y cálculo de métricas.
Orquesta la validación de intentos y calcula estadísticas para los reportes.
"""

from typing import Dict, List, Tuple
from models import Jugador, Tablero, Intento
from validator import SudokuValidator


class SudokuProcessor:
    """
    Clase que procesa los datos del torneo y calcula métricas de desempeño.
    """
    
    def __init__(self):
        """Inicializa el procesador con listas vacías."""
        self.jugadores: Dict[int, Jugador] = {}
        self.tableros: Dict[int, Tablero] = {}
        self.intentos: List[Intento] = []
        self.intentos_validados: List[Intento] = []
    
    def cargar_jugadores(self, jugadores: List[Jugador]) -> None:
        """
        Carga la lista de jugadores en el procesador.
        
        Args:
            jugadores (List[Jugador]): Lista de objetos Jugador.
        """
        for jugador in jugadores:
            self.jugadores[jugador.carnet] = jugador
    
    def cargar_tableros(self, tableros: List[Tablero]) -> None:
        """
        Carga la lista de tableros en el procesador.
        
        Args:
            tableros (List[Tablero]): Lista de objetos Tablero.
        """
        for tablero in tableros:
            self.tableros[tablero.id_sudoku] = tablero
    
    def cargar_intentos(self, intentos: List[Intento]) -> None:
        """
        Carga la lista de intentos en el procesador.
        
        Args:
            intentos (List[Intento]): Lista de objetos Intento.
        """
        self.intentos = intentos
    
    def validar_todos_intentos(self) -> int:
        """
        Valida todos los intentos cargados.
        
        Returns:
            int: Número de intentos validados.
        """
        self.intentos_validados = []
        
        for intento in self.intentos:
            # Buscar el tablero correspondiente
            tablero = self.tableros.get(intento.sudoku_id)
            
            if tablero is None:
                # Si no se encuentra el tablero, marcar como inválido
                intento.porcentaje_validez = 0.0
                intento.es_correcto = False
                intento.celdas_modificadas = []
                self.intentos_validados.append(intento)
                continue
            
            # Validar el intento
            resultado = SudokuValidator.validar_intento(
                tablero.tablero_inicial,
                intento.solucion
            )
            
            # Actualizar el intento con los resultados
            intento.porcentaje_validez = resultado['porcentaje_validez']
            intento.es_correcto = resultado['es_correcto']
            intento.celdas_modificadas = resultado['celdas_modificadas']
            
            self.intentos_validados.append(intento)
        
        return len(self.intentos_validados)
    
    def obtener_resumen_sudokus(self) -> Dict[int, Dict]:
        """
        Calcula el resumen por Sudoku.
        
        Returns:
            Dict[int, Dict]: Diccionario con estadísticas por Sudoku.
        """
        resumen = {}
        
        # Inicializar estadísticas para cada tablero
        for tablero_id, tablero in self.tableros.items():
            resumen[tablero_id] = {
                'id_sudoku': tablero_id,
                'dificultad': tablero.dificultad,
                'total_intentos': 0,
                'intentos_correctos': 0,
                'suma_tiempos': 0,
                'tiempo_promedio': 0.0,
                'tasa_exito': 0.0,
                'porcentaje_validez_promedio': 0.0,
                'suma_porcentajes': 0.0
            }
        
        # Procesar intentos validados
        for intento in self.intentos_validados:
            if intento.sudoku_id in resumen:
                stats = resumen[intento.sudoku_id]
                stats['total_intentos'] += 1
                stats['suma_tiempos'] += intento.tiempo_segundos
                stats['suma_porcentajes'] += intento.porcentaje_validez
                
                if intento.es_correcto:
                    stats['intentos_correctos'] += 1
        
        # Calcular promedios y tasas
        for stats in resumen.values():
            if stats['total_intentos'] > 0:
                stats['tiempo_promedio'] = stats['suma_tiempos'] / stats['total_intentos']
                stats['tasa_exito'] = (stats['intentos_correctos'] / stats['total_intentos']) * 100
                stats['porcentaje_validez_promedio'] = stats['suma_porcentajes'] / stats['total_intentos']
        
        return resumen
    
    def obtener_rendimiento_jugadores(self) -> Dict[int, Dict]:
        """
        Calcula el rendimiento por jugador.
        
        Returns:
            Dict[int, Dict]: Diccionario con estadísticas por jugador.
        """
        rendimiento = {}
        
        # Inicializar estadísticas para cada jugador
        for carnet, jugador in self.jugadores.items():
            rendimiento[carnet] = {
                'carnet': carnet,
                'nombre': jugador.nombre,
                'apellido': jugador.apellido,
                'nombre_completo': jugador.nombre_completo(),
                'nivel': jugador.nivel,
                'total_intentos': 0,
                'intentos_correctos': 0,
                'suma_tiempos': 0,
                'suma_porcentajes': 0,
                'tiempo_promedio': 0.0,
                'porcentaje_validez_promedio': 0.0,
                'tasa_exito': 0.0
            }
        
        # Procesar intentos validados
        for intento in self.intentos_validados:
            if intento.jugador_carnet in rendimiento:
                stats = rendimiento[intento.jugador_carnet]
                stats['total_intentos'] += 1
                stats['suma_tiempos'] += intento.tiempo_segundos
                stats['suma_porcentajes'] += intento.porcentaje_validez
                
                if intento.es_correcto:
                    stats['intentos_correctos'] += 1
        
        # Calcular promedios y tasas
        for stats in rendimiento.values():
            if stats['total_intentos'] > 0:
                stats['tiempo_promedio'] = stats['suma_tiempos'] / stats['total_intentos']
                stats['porcentaje_validez_promedio'] = stats['suma_porcentajes'] / stats['total_intentos']
                stats['tasa_exito'] = (stats['intentos_correctos'] / stats['total_intentos']) * 100
        
        return rendimiento
    
    def obtener_top10_tiempos(self) -> List[Dict]:
        """
        Obtiene los 10 mejores tiempos entre intentos correctos.
        
        Returns:
            List[Dict]: Lista de los 10 mejores intentos.
        """
        # Filtrar intentos correctos
        intentos_correctos = [i for i in self.intentos_validados if i.es_correcto]
        
        # Ordenar por tiempo (menor a mayor)
        intentos_correctos.sort(key=lambda x: x.tiempo_segundos)
        
        # Tomar los primeros 10
        top10 = intentos_correctos[:10]
        
        # Preparar datos para el reporte
        resultado = []
        for i, intento in enumerate(top10, 1):
            jugador = self.jugadores.get(intento.jugador_carnet)
            tablero = self.tableros.get(intento.sudoku_id)
            
            if jugador and tablero:
                resultado.append({
                    'posicion': i,
                    'carnet': jugador.carnet,
                    'nombre_completo': jugador.nombre_completo(),
                    'id_sudoku': tablero.id_sudoku,
                    'dificultad': tablero.dificultad,
                    'tiempo_segundos': intento.tiempo_segundos,
                    'fecha': intento.fecha
                })
        
        return resultado
    
    def obtener_estadisticas_generales(self) -> Dict:
        """
        Calcula estadísticas generales del torneo.
        
        Returns:
            Dict: Estadísticas generales.
        """
        total_intentos = len(self.intentos_validados)
        intentos_correctos = sum(1 for i in self.intentos_validados if i.es_correcto)
        
        if total_intentos > 0:
            tasa_exito_general = (intentos_correctos / total_intentos) * 100
            porcentaje_validez_promedio = sum(i.porcentaje_validez for i in self.intentos_validados) / total_intentos
            tiempo_promedio_general = sum(i.tiempo_segundos for i in self.intentos_validados) / total_intentos
        else:
            tasa_exito_general = 0.0
            porcentaje_validez_promedio = 0.0
            tiempo_promedio_general = 0.0
        
        return {
            'total_jugadores': len(self.jugadores),
            'total_tableros': len(self.tableros),
            'total_intentos': total_intentos,
            'intentos_correctos': intentos_correctos,
            'tasa_exito_general': tasa_exito_general,
            'porcentaje_validez_promedio': porcentaje_validez_promedio,
            'tiempo_promedio_general': tiempo_promedio_general
        }