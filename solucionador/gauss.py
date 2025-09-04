def _cero(x, e=1e-12): 
    return abs(x) <= e   # Verifica si x es prácticamente cero

def gauss_jordan(A_in):
    A = [f[:] for f in A_in]              # Copia de la matriz de entrada
    m, n = len(A), len(A[0]) - 1          # m = filas, n = columnas de A
    r = 0                                 # Índice de fila pivote

    for c in range(n):                    # Recorre columnas
        piv = next((i for i in range(r, m) if not _cero(A[i][c])), None)  # Busca pivote
        if piv is None: continue          # Si no hay pivote en esta columna, pasa
        if piv != r: A[r], A[piv] = A[piv], A[r]  # Intercambia filas si es necesario
        pv = A[r][c]                      # Valor del pivote
        for j in range(c, n+1): A[r][j] /= pv  # Normaliza fila pivote
        for i in range(m):                # Elimina otras entradas en la columna
            if i == r or _cero(A[i][c]): continue
            f = A[i][c]
            for j in range(c, n+1): 
                A[i][j] -= f * A[r][j]
        r += 1
        if r == m: break                  # Si se procesaron todas las filas, salir

    # Revisa si hay fila 0...0 | ≠0 → sistema inconsistente
    for i in range(m):
        if all(_cero(A[i][j]) for j in range(n)) and not _cero(A[i][n]):
            return "inconsistente", A

    # Rango de A (filas no nulas en las n primeras columnas)
    rango = sum(1 for i in range(m) if any(not _cero(A[i][j]) for j in range(n)))
    if rango < n: return "infinitas", A   # Menos pivotes que incógnitas → infinitas soluciones
    return "unica", A                     # Caso contrario → solución única


def leer_solucion_unica(A, e=1e-12):
    n, m = len(A[0]) - 1, len(A)          # n = incógnitas, m = filas
    sol = [None]*n                        # Lista de soluciones
    for j in range(n):                    # Recorre cada columna de incógnita
        fila = next((r for r in range(m)  # Busca fila donde columna j sea pivote
                     if abs(A[r][j]-1.0)<=e and all(abs(A[k][j])<=e for k in range(m) if k!=r)), None)
        if fila is not None: 
            sol[j] = A[fila][n]           # Asigna valor de b en esa fila
    return sol
