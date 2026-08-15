"""
main.py
Archivo principal del sistema de validación de Sudoku.
Contiene el menú interactivo y la lógica de carga de archivos.
"""

import os
import sys
from typing import List
from models import Jugador, Tablero, Intento
from processor import SudokuProcessor
from report_generator import ReportGenerator


class SudokuApp:
    """
    Clase principal de la aplicación de Sudoku.
    Maneja el menú interactivo y la carga de archivos.
    """
    
    def __init__(self):
        """Inicializa la aplicación."""
        self.processor = SudokuProcessor()
        self.report_generator = ReportGenerator(self.processor)
        
        # Bandera para verificar si los datos están cargados y validados
        self.datos_cargados = False
        self.intentos_validados = False
        
        # Menú principal
        self.menu_opciones = {
            '1': self.cargar_sudokus,
            '2': self.cargar_jugadores,
            '3': self.cargar_intentos,
            '4': self.validar_intentos,
            '5': self.generar_reporte_sudokus,
            '6': self.generar_reporte_jugadores,
            '7': self.generar_reporte_top10,
            '8': self.salir
        }
    
    def mostrar_menu(self):
        """Muestra el menú principal en consola."""
        print("\n" + "=" * 60)
        print("     TORNEO DE SUDOKU - NUMERIX ACADEMY")
        print("=" * 60)
        print("  1. Cargar archivo de sudokus")
        print("  2. Cargar archivo de jugadores")
        print("  3. Cargar archivo de intentos")
        print("  4. Validar y calificar intentos")
        print("  5. Generar Reporte: Resumen por Sudoku")
        print("  6. Generar Reporte: Rendimiento por Jugador")
        print("  7. Generar Reporte: Top 10 Mejores Tiempos")
        print("  8. Salir")
        print("=" * 60)
        
        # Mostrar estado de la aplicación
        if self.datos_cargados:
            print(f"📁 Datos cargados: Sí")
            if self.intentos_validados:
                print(f"✅ Intentos validados: Sí")
            else:
                print(f"⏳ Intentos validados: No")
        else:
            print(f"📁 Datos cargados: No")
        
        print("=" * 60)
    
    def ejecutar(self):
        """Ejecuta la aplicación en un bucle infinito."""
        while True:
            self.mostrar_menu()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion in self.menu_opciones:
                self.menu_opciones[opcion]()
            else:
                print("\n❌ Opción inválida. Por favor, seleccione una opción del 1 al 8.")
    
    def cargar_sudokus(self):
        """Carga el archivo de sudokus."""
        print("\n" + "-" * 40)
        print("  CARGAR ARCHIVO DE SUDOKUS")
        print("-" * 40)
        
        nombre_archivo = input("Ingrese el nombre del archivo (ej: sudokus.lfp): ").strip()
        
        if not os.path.exists(nombre_archivo):
            print(f"\n❌ Error: El archivo '{nombre_archivo}' no existe.")
            return
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            
            tableros = []
            for num_linea, linea in enumerate(lineas, 1):
                linea = linea.strip()
                if not linea:  # Saltar líneas vacías
                    continue
                
                try:
                    partes = linea.split(',')
                    if len(partes) != 3:
                        print(f"⚠️ Línea {num_linea}: Formato incorrecto (se esperaban 3 campos)")
                        continue
                    
                    id_sudoku = int(partes[0].strip())
                    dificultad = partes[1].strip()
                    cadena_tablero = partes[2].strip()
                    
                    tablero = Tablero(id_sudoku, dificultad, cadena_tablero)
                    tableros.append(tablero)
                    
                except ValueError as e:
                    print(f"⚠️ Línea {num_linea}: Error de conversión - {str(e)}")
                except Exception as e:
                    print(f"⚠️ Línea {num_linea}: Error - {str(e)}")
            
            if tableros:
                self.processor.cargar_tableros(tableros)
                self.datos_cargados = True
                print(f"\n✅ Se cargaron {len(tableros)} sudokus correctamente.")
            else:
                print("\n❌ No se pudo cargar ningún sudoku.")
                
        except FileNotFoundError:
            print(f"\n❌ Error: El archivo '{nombre_archivo}' no fue encontrado.")
        except Exception as e:
            print(f"\n❌ Error al leer el archivo: {str(e)}")
    
    def cargar_jugadores(self):
        """Carga el archivo de jugadores."""
        print("\n" + "-" * 40)
        print("  CARGAR ARCHIVO DE JUGADORES")
        print("-" * 40)
        
        nombre_archivo = input("Ingrese el nombre del archivo (ej: jugadores.lfp): ").strip()
        
        if not os.path.exists(nombre_archivo):
            print(f"\n❌ Error: El archivo '{nombre_archivo}' no existe.")
            return
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            
            jugadores = []
            for num_linea, linea in enumerate(lineas, 1):
                linea = linea.strip()
                if not linea:
                    continue
                
                try:
                    partes = linea.split(',')
                    if len(partes) != 4:
                        print(f"⚠️ Línea {num_linea}: Formato incorrecto (se esperaban 4 campos)")
                        continue
                    
                    carnet = int(partes[0].strip())
                    nombre = partes[1].strip()
                    apellido = partes[2].strip()
                    nivel = partes[3].strip()
                    
                    jugador = Jugador(carnet, nombre, apellido, nivel)
                    jugadores.append(jugador)
                    
                except ValueError as e:
                    print(f"⚠️ Línea {num_linea}: Error de conversión - {str(e)}")
                except Exception as e:
                    print(f"⚠️ Línea {num_linea}: Error - {str(e)}")
            
            if jugadores:
                self.processor.cargar_jugadores(jugadores)
                self.datos_cargados = True
                print(f"\n✅ Se cargaron {len(jugadores)} jugadores correctamente.")
            else:
                print("\n❌ No se pudo cargar ningún jugador.")
                
        except FileNotFoundError:
            print(f"\n❌ Error: El archivo '{nombre_archivo}' no fue encontrado.")
        except Exception as e:
            print(f"\n❌ Error al leer el archivo: {str(e)}")
    
    def cargar_intentos(self):
        """Carga el archivo de intentos."""
        print("\n" + "-" * 40)
        print("  CARGAR ARCHIVO DE INTENTOS")
        print("-" * 40)
        
        nombre_archivo = input("Ingrese el nombre del archivo (ej: intentos.lfp): ").strip()
        
        if not os.path.exists(nombre_archivo):
            print(f"\n❌ Error: El archivo '{nombre_archivo}' no existe.")
            return
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            
            intentos = []
            for num_linea, linea in enumerate(lineas, 1):
                linea = linea.strip()
                if not linea:
                    continue
                
                try:
                    partes = linea.split(',')
                    if len(partes) != 5:
                        print(f"⚠️ Línea {num_linea}: Formato incorrecto (se esperaban 5 campos)")
                        continue
                    
                    carnet = int(partes[0].strip())
                    id_sudoku = int(partes[1].strip())
                    solucion = partes[2].strip()
                    tiempo = int(partes[3].strip())
                    fecha = partes[4].strip()
                    
                    intento = Intento(carnet, id_sudoku, solucion, tiempo, fecha)
                    intentos.append(intento)
                    
                except ValueError as e:
                    print(f"⚠️ Línea {num_linea}: Error de conversión - {str(e)}")
                except Exception as e:
                    print(f"⚠️ Línea {num_linea}: Error - {str(e)}")
            
            if intentos:
                self.processor.cargar_intentos(intentos)
                self.datos_cargados = True
                print(f"\n✅ Se cargaron {len(intentos)} intentos correctamente.")
            else:
                print("\n❌ No se pudo cargar ningún intento.")
                
        except FileNotFoundError:
            print(f"\n❌ Error: El archivo '{nombre_archivo}' no fue encontrado.")
        except Exception as e:
            print(f"\n❌ Error al leer el archivo: {str(e)}")
    
    def validar_intentos(self):
        """Valida todos los intentos cargados."""
        print("\n" + "-" * 40)
        print("  VALIDAR Y CALIFICAR INTENTOS")
        print("-" * 40)
        
        if not self.datos_cargados:
            print("\n❌ Error: Primero debe cargar los archivos (opciones 1, 2 y 3).")
            return
        
        if not self.processor.intentos:
            print("\n❌ Error: No hay intentos cargados para validar.")
            return
        
        print("\n⏳ Validando intentos...")
        
        try:
            total_validados = self.processor.validar_todos_intentos()
            self.intentos_validados = True
            
            # Contar resultados
            correctos = sum(1 for i in self.processor.intentos_validados if i.es_correcto)
            
            print(f"\n✅ Validación completada.")
            print(f"   - Total de intentos validados: {total_validados}")
            print(f"   - Intentos correctos: {correctos}")
            print(f"   - Intentos incorrectos: {total_validados - correctos}")
            
            if total_validados > 0:
                porcentaje_correctos = (correctos / total_validados) * 100
                print(f"   - Tasa de éxito: {porcentaje_correctos:.2f}%")
            
        except Exception as e:
            print(f"\n❌ Error durante la validación: {str(e)}")
    
    def generar_reporte_sudokus(self):
        """Genera el reporte de resumen por Sudoku."""
        print("\n" + "-" * 40)
        print("  GENERAR REPORTE: RESUMEN POR SUDOKU")
        print("-" * 40)
        
        if not self.datos_cargados or not self.intentos_validados:
            print("\n❌ Error: Primero debe cargar los archivos y validar los intentos (opciones 1-4).")
            return
        
        try:
            ruta = self.report_generator.generar_reporte_sudokus()
            print(f"\n✅ Reporte generado exitosamente.")
            print(f"📁 Ubicación: {ruta}")
        except Exception as e:
            print(f"\n❌ Error al generar el reporte: {str(e)}")
    
    def generar_reporte_jugadores(self):
        """Genera el reporte de rendimiento por jugador."""
        print("\n" + "-" * 40)
        print("  GENERAR REPORTE: RENDIMIENTO POR JUGADOR")
        print("-" * 40)
        
        if not self.datos_cargados or not self.intentos_validados:
            print("\n❌ Error: Primero debe cargar los archivos y validar los intentos (opciones 1-4).")
            return
        
        try:
            ruta = self.report_generator.generar_reporte_jugadores()
            print(f"\n✅ Reporte generado exitosamente.")
            print(f"📁 Ubicación: {ruta}")
        except Exception as e:
            print(f"\n❌ Error al generar el reporte: {str(e)}")
    
    def generar_reporte_top10(self):
        """Genera el reporte de Top 10 mejores tiempos."""
        print("\n" + "-" * 40)
        print("  GENERAR REPORTE: TOP 10 MEJORES TIEMPOS")
        print("-" * 40)
        
        if not self.datos_cargados or not self.intentos_validados:
            print("\n❌ Error: Primero debe cargar los archivos y validar los intentos (opciones 1-4).")
            return
        
        try:
            ruta = self.report_generator.generar_reporte_top10()
            print(f"\n✅ Reporte generado exitosamente.")
            print(f"📁 Ubicación: {ruta}")
        except Exception as e:
            print(f"\n❌ Error al generar el reporte: {str(e)}")
    
    def salir(self):
        """Sale del programa."""
        print("\n" + "=" * 60)
        print("  ¡Gracias por usar el sistema de validación de Sudoku!")
        print("  Numerix Academy - Torneo de Sudoku")
        print("=" * 60)
        sys.exit(0)


def main():
    """Punto de entrada principal de la aplicación."""
    app = SudokuApp()
    app.ejecutar()


if __name__ == "__main__":
    main()