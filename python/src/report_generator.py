"""
report_generator.py
Módulo que genera los reportes en formato HTML.
"""

import os
from datetime import datetime
from typing import Dict, List
from processor import SudokuProcessor


class ReportGenerator:
    """
    Clase que genera reportes HTML a partir de los datos procesados.
    """
    
    def __init__(self, processor: SudokuProcessor):
        """
        Inicializa el generador de reportes.
        
        Args:
            processor (SudokuProcessor): Procesador con los datos cargados.
        """
        self.processor = processor
        self.reports_dir = "reports"
        
        # Crear directorio de reportes si no existe
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def _generar_html_base(self, titulo: str, contenido: str, estilo_extra: str = "") -> str:
        """
        Genera la estructura base de un documento HTML.
        
        Args:
            titulo (str): Título de la página.
            contenido (str): Contenido HTML del cuerpo.
            estilo_extra (str): Estilo CSS adicional.
            
        Returns:
            str: Documento HTML completo.
        """
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{titulo}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 15px;
                    margin-bottom: 30px;
                }}
                .header-info {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 25px;
                    border-left: 4px solid #3498db;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-bottom: 30px;
                }}
                .stat-card {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    border: 1px solid #e9ecef;
                }}
                .stat-value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .stat-label {{
                    color: #6c757d;
                    font-size: 14px;
                    margin-top: 5px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th {{
                    background: #3498db;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }}
                td {{
                    padding: 10px 12px;
                    border-bottom: 1px solid #e9ecef;
                }}
                tr:hover {{
                    background: #f8f9fa;
                }}
                .badge {{
                    display: inline-block;
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .badge-success {{
                    background: #d4edda;
                    color: #155724;
                }}
                .badge-danger {{
                    background: #f8d7da;
                    color: #721c24;
                }}
                .badge-warning {{
                    background: #fff3cd;
                    color: #856404;
                }}
                .badge-info {{
                    background: #d1ecf1;
                    color: #0c5460;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #6c757d;
                    font-size: 14px;
                    border-top: 1px solid #e9ecef;
                    padding-top: 20px;
                }}
                .no-data {{
                    text-align: center;
                    padding: 40px;
                    color: #6c757d;
                }}
                {estilo_extra}
            </style>
        </head>
        <body>
            <div class="container">
                {contenido}
                <div class="footer">
                    <p>Reporte generado el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}</p>
                    <p>Torneo de Sudoku - Numerix Academy</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def generar_reporte_sudokus(self, nombre_archivo: str = "reporte_sudokus.html") -> str:
        """
        Genera el Reporte 1: Resumen por Sudoku.
        
        Args:
            nombre_archivo (str): Nombre del archivo HTML a generar.
            
        Returns:
            str: Ruta del archivo generado.
        """
        resumen = self.processor.obtener_resumen_sudokus()
        
        if not resumen:
            contenido = """
            <div class="no-data">
                <h2>No hay datos disponibles</h2>
                <p>Por favor, cargue los archivos y valide los intentos primero.</p>
            </div>
            """
        else:
            # Estadísticas generales
            stats_generales = self.processor.obtener_estadisticas_generales()
            
            contenido = f"""
            <h1>📊 Resumen por Sudoku</h1>
            
            <div class="header-info">
                <p><strong>Total de Sudokus:</strong> {len(resumen)}</p>
                <p><strong>Total de Intentos:</strong> {stats_generales['total_intentos']}</p>
                <p><strong>Tasa de Éxito General:</strong> {stats_generales['tasa_exito_general']:.2f}%</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Dificultad</th>
                        <th>Intentos</th>
                        <th>Correctos</th>
                        <th>Tasa de Éxito</th>
                        <th>Tiempo Promedio (s)</th>
                        <th>Validez Promedio (%)</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            # Ordenar por ID
            for sudoku_id in sorted(resumen.keys()):
                stats = resumen[sudoku_id]
                
                # Colores según dificultad
                colores_dificultad = {
                    'Facil': 'badge-success',
                    'Media': 'badge-info',
                    'Difícil': 'badge-warning',
                    'Experto': 'badge-danger'
                }
                badge_class = colores_dificultad.get(stats['dificultad'], 'badge-info')
                
                contenido += f"""
                    <tr>
                        <td><strong>#{stats['id_sudoku']}</strong></td>
                        <td><span class="badge {badge_class}">{stats['dificultad']}</span></td>
                        <td>{stats['total_intentos']}</td>
                        <td>{stats['intentos_correctos']}</td>
                        <td>{stats['tasa_exito']:.1f}%</td>
                        <td>{stats['tiempo_promedio']:.1f}</td>
                        <td>{stats['porcentaje_validez_promedio']:.1f}%</td>
                    </tr>
                """
            
            contenido += """
                </tbody>
            </table>
            """
        
        html_completo = self._generar_html_base(
            "Resumen por Sudoku - Numerix Academy",
            contenido
        )
        
        # Guardar archivo
        ruta_archivo = os.path.join(self.reports_dir, nombre_archivo)
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(html_completo)
        
        return ruta_archivo
    
    def generar_reporte_jugadores(self, nombre_archivo: str = "reporte_jugadores.html") -> str:
        """
        Genera el Reporte 2: Rendimiento por Jugador.
        
        Args:
            nombre_archivo (str): Nombre del archivo HTML a generar.
            
        Returns:
            str: Ruta del archivo generado.
        """
        rendimiento = self.processor.obtener_rendimiento_jugadores()
        
        if not rendimiento:
            contenido = """
            <div class="no-data">
                <h2>No hay datos disponibles</h2>
                <p>Por favor, cargue los archivos y valide los intentos primero.</p>
            </div>
            """
        else:
            stats_generales = self.processor.obtener_estadisticas_generales()
            
            contenido = f"""
            <h1>🏆 Rendimiento por Jugador</h1>
            
            <div class="header-info">
                <p><strong>Total de Jugadores:</strong> {stats_generales['total_jugadores']}</p>
                <p><strong>Total de Intentos:</strong> {stats_generales['total_intentos']}</p>
                <p><strong>Porcentaje de Validez Promedio:</strong> {stats_generales['porcentaje_validez_promedio']:.2f}%</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Jugador</th>
                        <th>Carnet</th>
                        <th>Nivel</th>
                        <th>Intentos</th>
                        <th>Correctos</th>
                        <th>Tasa de Éxito</th>
                        <th>Tiempo Promedio (s)</th>
                        <th>Validez Promedio (%)</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            # Ordenar por nombre
            jugadores_ordenados = sorted(rendimiento.values(), key=lambda x: x['nombre'])
            
            for jugador in jugadores_ordenados:
                # Colores según nivel
                colores_nivel = {
                    'Principiante': 'badge-info',
                    'Intermedio': 'badge-warning',
                    'Experto': 'badge-success'
                }
                badge_class = colores_nivel.get(jugador['nivel'], 'badge-info')
                
                # Destacar los mejores
                estilo_fila = ""
                if jugador['tasa_exito'] >= 80:
                    estilo_fila = ' style="background-color: #d4edda;"'
                
                contenido += f"""
                    <tr{estilo_fila}>
                        <td><strong>{jugador['nombre_completo']}</strong></td>
                        <td>{jugador['carnet']}</td>
                        <td><span class="badge {badge_class}">{jugador['nivel']}</span></td>
                        <td>{jugador['total_intentos']}</td>
                        <td>{jugador['intentos_correctos']}</td>
                        <td>{jugador['tasa_exito']:.1f}%</td>
                        <td>{jugador['tiempo_promedio']:.1f}</td>
                        <td>{jugador['porcentaje_validez_promedio']:.1f}%</td>
                    </tr>
                """
            
            contenido += """
                </tbody>
            </table>
            """
        
        html_completo = self._generar_html_base(
            "Rendimiento por Jugador - Numerix Academy",
            contenido
        )
        
        ruta_archivo = os.path.join(self.reports_dir, nombre_archivo)
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(html_completo)
        
        return ruta_archivo
    
    def generar_reporte_top10(self, nombre_archivo: str = "reporte_top10.html") -> str:
        """
        Genera el Reporte 3: Top 10 Mejores Tiempos.
        
        Args:
            nombre_archivo (str): Nombre del archivo HTML a generar.
            
        Returns:
            str: Ruta del archivo generado.
        """
        top10 = self.processor.obtener_top10_tiempos()
        
        if not top10:
            contenido = """
            <div class="no-data">
                <h2>No hay datos disponibles</h2>
                <p>No se encontraron intentos resueltos correctamente.</p>
            </div>
            """
        else:
            # Medallas para los primeros 3
            medallas = ['🥇', '🥈', '🥉']
            
            contenido = f"""
            <h1>⏱️ Top 10 Mejores Tiempos</h1>
            
            <div class="header-info">
                <p><strong>Total de intentos correctos:</strong> {len([i for i in self.processor.intentos_validados if i.es_correcto])}</p>
                <p><strong>Mejor tiempo:</strong> {top10[0]['tiempo_segundos']} segundos</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Posición</th>
                        <th>Jugador</th>
                        <th>Carnet</th>
                        <th>Sudoku</th>
                        <th>Dificultad</th>
                        <th>Tiempo (s)</th>
                        <th>Fecha</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for intento in top10:
                medalla = medallas[intento['posicion'] - 1] if intento['posicion'] <= 3 else f"#{intento['posicion']}"
                
                # Destacar el primer lugar
                estilo_fila = ' style="background-color: #fff3cd;"' if intento['posicion'] == 1 else ''
                
                colores_dificultad = {
                    'Facil': 'badge-success',
                    'Media': 'badge-info',
                    'Difícil': 'badge-warning',
                    'Experto': 'badge-danger'
                }
                badge_class = colores_dificultad.get(intento['dificultad'], 'badge-info')
                
                contenido += f"""
                    <tr{estilo_fila}>
                        <td><strong>{medalla}</strong></td>
                        <td><strong>{intento['nombre_completo']}</strong></td>
                        <td>{intento['carnet']}</td>
                        <td>#{intento['id_sudoku']}</td>
                        <td><span class="badge {badge_class}">{intento['dificultad']}</span></td>
                        <td><strong>{intento['tiempo_segundos']}</strong></td>
                        <td>{intento['fecha']}</td>
                    </tr>
                """
            
            contenido += """
                </tbody>
            </table>
            """
        
        html_completo = self._generar_html_base(
            "Top 10 Mejores Tiempos - Numerix Academy",
            contenido
        )
        
        ruta_archivo = os.path.join(self.reports_dir, nombre_archivo)
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(html_completo)
        
        return ruta_archivo