"""
validator.py
Módulo que contiene la lógica de validación del Sudoku.
Implementa la verificación de pistas originales, filas, columnas y cajas de 3x3.
"""

class SudokuValidator:
    """
    Clase que contiene la lógica de validación para intentos de Sudoku.
    Proporciona métodos estáticos para validar pistas, unidades y intentos completos.
    """
    
    @staticmethod
    def validar_pistas_originales(tablero_original: list, solucion_propuesta: list) -> tuple:
        """
        Verifica que las pistas originales no hayan sido modificadas en la solución propuesta.
        
        Args:
            tablero_original (list): Matriz 9x9 del tablero original.
            solucion_propuesta (list): Matriz 9x9 de la solución propuesta.
            
        Returns:
            tuple: (bool, list) - (True si todas las pistas se respetaron, lista de celdas modificadas)
        """
        celdas_modificadas = []
        
        for i in range(9):
            for j in range(9):
                # Si es una pista (valor != 0) y fue modificada
                if tablero_original[i][j] != 0 and tablero_original[i][j] != solucion_propuesta[i][j]:
                    celdas_modificadas.append((i, j))
        
        return len(celdas_modificadas) == 0, celdas_modificadas
    
    @staticmethod
    def _obtener_unidad(matriz: list, tipo: str, indice: int) -> list:
        """
        Obtiene una unidad específica (fila, columna o caja) de la matriz.
        
        Args:
            matriz (list): Matriz 9x9.
            tipo (str): Tipo de unidad ('fila', 'columna', 'caja').
            indice (int): Índice de la unidad (0-8).
            
        Returns:
            list: Lista de 9 elementos de la unidad solicitada.
            
        Raises:
            ValueError: Si el tipo no es válido.
        """
        if tipo == 'fila':
            return matriz[indice][:]
        
        elif tipo == 'columna':
            return [matriz[fila][indice] for fila in range(9)]
        
        elif tipo == 'caja':
            fila_inicio = (indice // 3) * 3
            col_inicio = (indice % 3) * 3
            unidad = []
            for i in range(fila_inicio, fila_inicio + 3):
                for j in range(col_inicio, col_inicio + 3):
                    unidad.append(matriz[i][j])
            return unidad
        
        else:
            raise ValueError(f"Tipo de unidad no válido: {tipo}. Debe ser 'fila', 'columna' o 'caja'.")
    
    @staticmethod
    def _unidad_es_valida(unidad: list) -> bool:
        """
        Verifica si una unidad (fila, columna o caja) es válida.
        Una unidad es válida si contiene los dígitos del 1 al 9 sin repetirse.
        
        Args:
            unidad (list): Lista de 9 elementos (puede contener ceros).
            
        Returns:
            bool: True si la unidad es válida, False en caso contrario.
        """
        # Filtrar los ceros (celdas vacías)
        digitos = [d for d in unidad if d != 0]
        
        # Verificar que todos los dígitos estén en el rango 1-9
        if not all(1 <= d <= 9 for d in digitos):
            return False
        
        # Verificar que no haya dígitos repetidos
        return len(digitos) == len(set(digitos))
    
    @staticmethod
    def validar_intento(tablero_original: list, solucion_propuesta: list) -> dict:
        """
        Valida completamente un intento de Sudoku.
        
        Args:
            tablero_original (list): Matriz 9x9 del tablero original.
            solucion_propuesta (list): Matriz 9x9 de la solución propuesta.
            
        Returns:
            dict: Diccionario con los resultados de la validación:
                - 'pistas_respetadas' (bool): True si todas las pistas se respetaron.
                - 'celdas_modificadas' (list): Lista de celdas donde se modificaron pistas.
                - 'unidades_validas' (int): Número de unidades válidas (0-27).
                - 'porcentaje_validez' (float): Porcentaje de validez (0-100).
                - 'es_correcto' (bool): True si el intento es completamente correcto.
                - 'detalles' (dict): Detalles por tipo de unidad.
        """
        resultado = {
            'pistas_respetadas': False,
            'celdas_modificadas': [],
            'unidades_validas': 0,
            'porcentaje_validez': 0.0,
            'es_correcto': False,
            'detalles': {
                'filas_validas': 0,
                'columnas_validas': 0,
                'cajas_validas': 0,
                'filas_invalidas': [],
                'columnas_invalidas': [],
                'cajas_invalidas': []
            }
        }
        
        # PASO 1: Verificar pistas originales
        pistas_respetadas, celdas_modificadas = SudokuValidator.validar_pistas_originales(
            tablero_original, solucion_propuesta
        )
        resultado['pistas_respetadas'] = pistas_respetadas
        resultado['celdas_modificadas'] = celdas_modificadas
        
        # Si no se respetaron las pistas, el intento es inválido
        if not pistas_respetadas:
            resultado['porcentaje_validez'] = 0.0
            resultado['es_correcto'] = False
            return resultado
        
        # PASO 2: Validar todas las unidades (filas, columnas y cajas)
        unidades_validas = 0
        
        # Validar filas (9)
        for i in range(9):
            fila = SudokuValidator._obtener_unidad(solucion_propuesta, 'fila', i)
            if SudokuValidator._unidad_es_valida(fila):
                unidades_validas += 1
                resultado['detalles']['filas_validas'] += 1
            else:
                resultado['detalles']['filas_invalidas'].append(i)
        
        # Validar columnas (9)
        for j in range(9):
            columna = SudokuValidator._obtener_unidad(solucion_propuesta, 'columna', j)
            if SudokuValidator._unidad_es_valida(columna):
                unidades_validas += 1
                resultado['detalles']['columnas_validas'] += 1
            else:
                resultado['detalles']['columnas_invalidas'].append(j)
        
        # Validar cajas (9)
        for k in range(9):
            caja = SudokuValidator._obtener_unidad(solucion_propuesta, 'caja', k)
            if SudokuValidator._unidad_es_valida(caja):
                unidades_validas += 1
                resultado['detalles']['cajas_validas'] += 1
            else:
                resultado['detalles']['cajas_invalidas'].append(k)
        
        resultado['unidades_validas'] = unidades_validas
        
        # PASO 3: Calcular porcentaje de validez
        resultado['porcentaje_validez'] = (unidades_validas / 27) * 100
        
        # PASO 4: Determinar si es correcto
        resultado['es_correcto'] = (pistas_respetadas and unidades_validas == 27)
        
        return resultado
    
    @staticmethod
    def validar_multiples_intentos(tableros_originales: dict, intentos: list) -> list:
        """
        Valida múltiples intentos en lote.
        
        Args:
            tableros_originales (dict): Diccionario {id_sudoku: tablero_original}.
            intentos (list): Lista de objetos Intento.
            
        Returns:
            list: Lista de objetos Intento con sus atributos de validación actualizados.
        """
        intentos_validados = []
        
        for intento in intentos:
            # Obtener el tablero original correspondiente
            tablero_original = tableros_originales.get(intento.sudoku_id)
            
            if tablero_original is None:
                # Si no se encuentra el tablero, marcar como inválido
                intento.porcentaje_validez = 0.0
                intento.es_correcto = False
                intento.celdas_modificadas = []
                intentos_validados.append(intento)
                continue
            
            # Validar el intento
            resultado = SudokuValidator.validar_intento(
                tablero_original.tablero_inicial,
                intento.solucion
            )
            
            # Actualizar el objeto Intento con los resultados
            intento.porcentaje_validez = resultado['porcentaje_validez']
            intento.es_correcto = resultado['es_correcto']
            intento.celdas_modificadas = resultado['celdas_modificadas']
            intento.detalles_validacion = resultado['detalles']  # Para depuración
            
            intentos_validados.append(intento)
        
        return intentos_validados


# Funciones auxiliares para uso directo (sin clase)
def validar_pistas_originales(tablero_original: list, solucion_propuesta: list) -> tuple:
    """
    Función auxiliar para validar pistas originales.
    
    Args:
        tablero_original (list): Matriz 9x9 del tablero original.
        solucion_propuesta (list): Matriz 9x9 de la solución propuesta.
        
    Returns:
        tuple: (bool, list) - (True si todas las pistas se respetaron, lista de celdas modificadas)
    """
    return SudokuValidator.validar_pistas_originales(tablero_original, solucion_propuesta)


def validar_intento(tablero_original: list, solucion_propuesta: list) -> dict:
    """
    Función auxiliar para validar un intento completo.
    
    Args:
        tablero_original (list): Matriz 9x9 del tablero original.
        solucion_propuesta (list): Matriz 9x9 de la solución propuesta.
        
    Returns:
        dict: Resultados de la validación.
    """
    return SudokuValidator.validar_intento(tablero_original, solucion_propuesta)