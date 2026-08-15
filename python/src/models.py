"""
models.py
Módulo que contiene las clases principales para el sistema de validación de Sudoku.
Define las entidades: Jugador, Tablero y Intento.
"""

class Jugador:
    """
    Clase que representa a un jugador del torneo.
    
    Atributos:
        carnet (int): Identificador único del jugador.
        nombre (str): Nombre del jugador.
        apellido (str): Apellido del jugador.
        nivel (str): Nivel de experiencia (Principiante, Intermedio, Experto).
    """
    
    def __init__(self, carnet: int, nombre: str, apellido: str, nivel: str):
        """
        Constructor de la clase Jugador.
        
        Args:
            carnet (int): Identificador único del jugador.
            nombre (str): Nombre del jugador.
            apellido (str): Apellido del jugador.
            nivel (str): Nivel de experiencia.
        """
        self.carnet = carnet
        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        self.nivel = nivel.strip()
    
    def nombre_completo(self) -> str:
        """
        Devuelve el nombre completo del jugador.
        
        Returns:
            str: Nombre completo (nombre + apellido).
        """
        return f"{self.nombre} {self.apellido}"
    
    def __str__(self) -> str:
        """
        Representación en string del jugador.
        
        Returns:
            str: Información del jugador en formato legible.
        """
        return f"Jugador: {self.nombre_completo()} (Carnet: {self.carnet}, Nivel: {self.nivel})"
    
    def __repr__(self) -> str:
        """
        Representación técnica del jugador.
        
        Returns:
            str: Representación para depuración.
        """
        return f"Jugador(carnet={self.carnet}, nombre='{self.nombre}', apellido='{self.apellido}', nivel='{self.nivel}')"


class Tablero:
    """
    Clase que representa un tablero de Sudoku.
    
    Atributos:
        id_sudoku (int): Identificador único del tablero.
        dificultad (str): Nivel de dificultad (Facil, Media, Difícil, Experto).
        tablero_inicial (list): Matriz 9x9 de enteros representando el tablero.
    """
    
    def __init__(self, id_sudoku: int, dificultad: str, cadena_tablero: str):
        """
        Constructor de la clase Tablero.
        
        Args:
            id_sudoku (int): Identificador único del tablero.
            dificultad (str): Nivel de dificultad.
            cadena_tablero (str): Cadena de 81 caracteres representando el tablero.
            
        Raises:
            ValueError: Si la cadena no tiene exactamente 81 caracteres.
        """
        self.id_sudoku = id_sudoku
        self.dificultad = dificultad.strip()
        self.tablero_inicial = self._cadena_a_matriz(cadena_tablero)
    
    def _cadena_a_matriz(self, cadena: str) -> list:
        """
        Convierte una cadena de 81 caracteres en una matriz de 9x9.
        
        Args:
            cadena (str): Cadena de 81 caracteres (dígitos 0-9).
            
        Returns:
            list: Matriz de 9x9 con valores enteros.
            
        Raises:
            ValueError: Si la cadena no tiene exactamente 81 caracteres.
        """
        # Limpiar la cadena (eliminar espacios en blanco)
        cadena = cadena.strip()
        
        if len(cadena) != 81:
            raise ValueError(f"La cadena debe tener exactamente 81 caracteres. Longitud actual: {len(cadena)}")
        
        matriz = []
        for i in range(9):
            fila = []
            for j in range(9):
                # Convertir cada caracter a entero
                try:
                    valor = int(cadena[i * 9 + j])
                    if not (0 <= valor <= 9):
                        raise ValueError(f"Caracter inválido en posición {i*9+j}: {cadena[i*9+j]}")
                    fila.append(valor)
                except ValueError:
                    raise ValueError(f"Caracter no numérico en posición {i*9+j}: {cadena[i*9+j]}")
            matriz.append(fila)
        
        return matriz
    
    def get_valor(self, fila: int, columna: int) -> int:
        """
        Devuelve el valor en una celda específica del tablero.
        
        Args:
            fila (int): Índice de la fila (0-8).
            columna (int): Índice de la columna (0-8).
            
        Returns:
            int: Valor en la celda (0 si está vacía).
            
        Raises:
            IndexError: Si los índices están fuera de rango.
        """
        if not (0 <= fila < 9 and 0 <= columna < 9):
            raise IndexError(f"Índices fuera de rango: fila={fila}, columna={columna}")
        return self.tablero_inicial[fila][columna]
    
    def es_pista(self, fila: int, columna: int) -> bool:
        """
        Verifica si una celda es una pista (valor fijo).
        
        Args:
            fila (int): Índice de la fila (0-8).
            columna (int): Índice de la columna (0-8).
            
        Returns:
            bool: True si la celda tiene un valor fijo (> 0), False en caso contrario.
        """
        return self.get_valor(fila, columna) != 0
    
    def __str__(self) -> str:
        """
        Representación en string del tablero.
        
        Returns:
            str: Tablero formateado para visualización.
        """
        resultado = f"Sudoku #{self.id_sudoku} - Dificultad: {self.dificultad}\n"
        resultado += "   " + " ".join(str(i) for i in range(9)) + "\n"
        resultado += "  " + "-" * 19 + "\n"
        
        for i, fila in enumerate(self.tablero_inicial):
            resultado += f"{i}| "
            for j, valor in enumerate(fila):
                resultado += str(valor) if valor != 0 else "."
                if j < 8:
                    resultado += " "
            resultado += " |\n"
        
        resultado += "  " + "-" * 19
        return resultado
    
    def __repr__(self) -> str:
        """
        Representación técnica del tablero.
        
        Returns:
            str: Representación para depuración.
        """
        return f"Tablero(id_sudoku={self.id_sudoku}, dificultad='{self.dificultad}')"


class Intento:
    """
    Clase que representa un intento de resolución de Sudoku.
    
    Atributos:
        jugador_carnet (int): Carnet del jugador que realizó el intento.
        sudoku_id (int): ID del tablero intentado.
        solucion (list): Matriz 9x9 con la solución propuesta.
        tiempo_segundos (int): Tiempo empleado en segundos.
        fecha (str): Fecha del intento (formato DD-MM-AAAA).
        porcentaje_validez (float): Porcentaje de validez del intento (calculado después).
        es_correcto (bool): Indica si el intento es correcto (calculado después).
    """
    
    def __init__(self, jugador_carnet: int, sudoku_id: int, cadena_solucion: str, 
                 tiempo_segundos: int, fecha: str):
        """
        Constructor de la clase Intento.
        
        Args:
            jugador_carnet (int): Carnet del jugador.
            sudoku_id (int): ID del tablero.
            cadena_solucion (str): Cadena de 81 caracteres con la solución propuesta.
            tiempo_segundos (int): Tiempo empleado en segundos.
            fecha (str): Fecha del intento en formato DD-MM-AAAA.
            
        Raises:
            ValueError: Si la cadena de solución no tiene exactamente 81 caracteres.
        """
        self.jugador_carnet = jugador_carnet
        self.sudoku_id = sudoku_id
        self.solucion = self._cadena_a_matriz(cadena_solucion)
        self.tiempo_segundos = tiempo_segundos
        self.fecha = fecha.strip()
        
        # Atributos que se calcularán durante la validación
        self.porcentaje_validez = 0.0
        self.es_correcto = False
        self.celdas_modificadas = []  # Lista de tuplas (fila, columna) donde se modificaron pistas
    
    def _cadena_a_matriz(self, cadena: str) -> list:
        """
        Convierte una cadena de 81 caracteres en una matriz de 9x9.
        
        Args:
            cadena (str): Cadena de 81 caracteres (dígitos 1-9).
            
        Returns:
            list: Matriz de 9x9 con valores enteros.
            
        Raises:
            ValueError: Si la cadena no tiene exactamente 81 caracteres.
        """
        cadena = cadena.strip()
        
        if len(cadena) != 81:
            raise ValueError(f"La cadena de solución debe tener exactamente 81 caracteres. Longitud actual: {len(cadena)}")
        
        matriz = []
        for i in range(9):
            fila = []
            for j in range(9):
                try:
                    valor = int(cadena[i * 9 + j])
                    if not (0 <= valor <= 9):
                        raise ValueError(f"Caracter inválido en posición {i*9+j}: {cadena[i*9+j]}")
                    fila.append(valor)
                except ValueError:
                    raise ValueError(f"Caracter no numérico en posición {i*9+j}: {cadena[i*9+j]}")
            matriz.append(fila)
        
        return matriz
    
    def get_solucion_valor(self, fila: int, columna: int) -> int:
        """
        Devuelve el valor en una celda específica de la solución.
        
        Args:
            fila (int): Índice de la fila (0-8).
            columna (int): Índice de la columna (0-8).
            
        Returns:
            int: Valor en la celda.
        """
        if not (0 <= fila < 9 and 0 <= columna < 9):
            raise IndexError(f"Índices fuera de rango: fila={fila}, columna={columna}")
        return self.solucion[fila][columna]
    
    def es_solucion_completa(self) -> bool:
        """
        Verifica si la solución no tiene celdas vacías.
        
        Returns:
            bool: True si no hay ceros en la solución.
        """
        for fila in self.solucion:
            for valor in fila:
                if valor == 0:
                    return False
        return True
    
    def __str__(self) -> str:
        """
        Representación en string del intento.
        
        Returns:
            str: Información del intento en formato legible.
        """
        estado = "Correcto" if self.es_correcto else "Incorrecto"
        return (f"Intento del jugador {self.jugador_carnet} en Sudoku #{self.sudoku_id} - "
                f"Tiempo: {self.tiempo_segundos}s - {self.porcentaje_validez:.2f}% válido - {estado}")
    
    def __repr__(self) -> str:
        """
        Representación técnica del intento.
        
        Returns:
            str: Representación para depuración.
        """
        return (f"Intento(jugador_carnet={self.jugador_carnet}, sudoku_id={self.sudoku_id}, "
                f"tiempo_segundos={self.tiempo_segundos}, fecha='{self.fecha}')")