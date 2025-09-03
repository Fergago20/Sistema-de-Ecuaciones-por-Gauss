from fractions import Fraction  # Importa la clase Fraction para trabajar con fracciones exactas

# Función para dar formato a una fracción o número
def formatear_fraccion(x: Fraction) -> str:
    if isinstance(x, Fraction):        # Si el valor es una fracción
        if x.denominator == 1:         # Si el denominador es 1, mostrar solo el numerador
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"  # Mostrar como "numerador/denominador"
    return str(x)  # Si no es fracción, convertir a string normal

# Función para calcular el ancho máximo de cada columna en la matriz
def _col_widths(mat):
    if not mat:  
        return []  # Si la matriz está vacía, devolver lista vacía
    cols = len(mat[0])          # Número de columnas de la primera fila
    w = [0]*cols                # Lista de anchos inicializada en 0
    for row in mat:             # Recorrer cada fila
        for j, val in enumerate(row):     # Recorrer cada valor con su índice de columna
            s = formatear_fraccion(val)             # Convertir el valor a string con formato
            w[j] = max(w[j], len(s))      # Actualizar el ancho máximo de esa columna
    return w  # Devolver lista con anchos de cada columna

# Función para generar una representación en texto de la matriz
def matriz_str(mat, titulo=None):
    if not mat:
        return "(matriz vacía)\n"  # Si la matriz está vacía, devolver mensaje
    widths = _col_widths(mat)      # Obtener anchos de columnas
    out = []
    if titulo:                     
        out.append(titulo)         # Agregar título si se proporciona
    for row in mat:                
        # Formatear cada celda con justificación a la derecha según el ancho de su columna
        cells = [formatear_fraccion(val).rjust(widths[j]) for j, val in enumerate(row)]
        # Construir fila en formato [ a  b  c ]
        out.append("[ " + "  ".join(cells) + " ]")
    return "\n".join(out) + "\n"   # Unir todas las filas en un solo string con saltos de línea
