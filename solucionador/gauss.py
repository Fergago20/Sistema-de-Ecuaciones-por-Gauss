from fractions import Fraction  # Usamos fracciones exactas


def _as_frac(x):
    """Convierte x a Fraction; rechaza float para mantener exactitud."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, float):
        raise TypeError("Prototipo exacto: solo enteros o fractions.Fraction (no float).")
    return Fraction(x)  # Conversión genérica (p.ej., desde cadenas o Decimals)


def _to_frac_matrix(A_in):
    """Copia la matriz y convierte cada celda a Fraction (copia por filas)."""
    return [[_as_frac(v) for v in fila] for fila in A_in]


def _cero(x):
    """Cero exacto """
    return x == 0


def gauss_jordan(A_in):
    """
    Gauss–Jordan exacto sobre matriz aumentada (m x (n+1)).
    Devuelve: ('inconsistente'|'infinitas'|'unica', matriz_reducida)
    """
    A = _to_frac_matrix(A_in)            # Trabajamos sobre una copia exacta
    m, n = len(A), len(A[0]) - 1         # m filas, n incógnitas
    r = 0                                # Próxima fila pivote

    for c in range(n):                   # Recorre columnas de variables
        # Buscar primer pivote no nulo en/abajo de r (sin pivoteo parcial)
        piv = next((i for i in range(r, m) if not _cero(A[i][c])), None)
        if piv is None:
            continue
        if piv != r:
            A[r], A[piv] = A[piv], A[r]  # Subir pivote a la fila r

        pv = A[r][c]
        # Normalizar fila pivote (hacer pivote = 1 y escalar el resto, incluida b)
        for j in range(c, n+1):
            A[r][j] = A[r][j] / pv

        # Eliminar la columna c en todas las demás filas
        for i in range(m):
            if i == r or _cero(A[i][c]):
                continue
            f = A[i][c]
            for j in range(c, n+1):
                A[i][j] = A[i][j] - f * A[r][j]

        r += 1
        if r == m:
            break  # No hay más filas disponibles para nuevos pivotes

    # Inconsistencia: fila [0 ... 0 | d] con d != 0  -> no hay solución
    for i in range(m):
        if all(_cero(A[i][j]) for j in range(n)) and not _cero(A[i][n]):
            return "inconsistente", A

    # Rango de la parte de coeficientes (cuántas filas no nulas quedan)
    rango = sum(1 for i in range(m) if any(not _cero(A[i][j]) for j in range(n)))
    if rango < n:
        return "infinitas", A            # Menos pivotes que variables -> parámetros libres
    return "unica", A                     # Mismo # de pivotes que variables -> solución única


def leer_solucion_unica(A):
    """
    Extrae el vector solución de una matriz en RREF con solución única.
    Retorna lista de Fraction, una por variable.
    """
    n, m = len(A[0]) - 1, len(A)
    sol = [None] * n
    UNO, CERO = Fraction(1), Fraction(0)

    for j in range(n):  # Para cada variable (columna)
        # Fila pivote en la columna j: 1 en (r,j) y 0 en el resto de esa columna
        fila = next(
            (r for r in range(m)
             if A[r][j] == UNO and all(A[k][j] == CERO for k in range(m) if k != r)),
            None
        )
        if fila is not None:
            sol[j] = A[fila][n]  # Término independiente de esa fila

    return sol
