from fractions import Fraction        # Permite trabajar con fracciones exactas (racionales)
from copy import deepcopy             # Para copiar matrices sin modificar el original
from .formats import matriz_str, formatear_fraccion   # Funciones auxiliares para dar formato e imprimir matrices

# Intercambia dos filas de la matriz A (i ↔ j)
def _swap(A, i, j):
    if i != j:                        # Solo intercambia si son distintas
        A[i], A[j] = A[j], A[i]       # Intercambio de filas
        return f"F{i+1} ↔ F{j+1}"     # Devuelve notación de la operación (ej: F1 ↔ F2)

# Escala una fila de la matriz A (multiplica la fila i por un escalar k)
def _scale(A, i, k: Fraction):
    if k == 0:                        # No se puede multiplicar por cero
        raise ZeroDivisionError("No se puede escalar por 0.")
    A[i] = [a * k for a in A[i]]      # Multiplica cada elemento de la fila
    return f"F{i+1} ← ({formatear_fraccion(k)})·F{i+1}"   # Notación de la operación

# Suma una fila a otra: F_t ← F_t + k·F_s
def _add(A, t, s, k: Fraction):
    A[t] = [A[t][c] + k * A[s][c] for c in range(len(A[0]))]  # Operación fila a fila
    return f"F{t+1} ← F{t+1} + ({formatear_fraccion(k)})·F{s+1}"        # Notación de la operación

# Algoritmo de Gauss-Jordan con registro de pasos
def gauss_jordan_con_log(A_in, log_fn=lambda s: None):
    """
    Lleva A a su forma escalonada reducida (RREF).
    Usa pivoteo simple (no elige el mayor por magnitud, lo mantiene didáctico).
    Retorna una tupla (tipo, A) donde tipo ∈ {"unica","infinitas","inconsistente"}.
    """
    A = deepcopy(A_in)                # Copiar matriz para no alterar la original
    m = len(A)                        # Número de filas
    n = len(A[0]) - 1                 # Número de columnas de coeficientes (última es b)

    log_fn(matriz_str(A, "Matriz inicial [A|b]"))  # Mostrar la matriz inicial

    r = 0  # Índice de fila activa (fila de pivote)
    for c in range(n):                # Recorre columnas de coeficientes
        # Buscar pivote ≠ 0 desde la fila r hacia abajo
        piv = None
        for i in range(r, m):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:               # Si no hay pivote en la columna, pasa a la siguiente
            continue

        # Intercambiar fila actual con la fila del pivote
        op = _swap(A, r, piv)
        if op:
            log_fn(f"Operación: {op}\n" + matriz_str(A))

        # Escalar la fila del pivote para que el pivote sea 1
        val = A[r][c]
        if val != 1:
            op = _scale(A, r, Fraction(1, 1) / val)
            log_fn(f"Operación: {op}\n" + matriz_str(A))

        # Hacer ceros en toda la columna excepto en el pivote
        for i in range(m):
            if i == r:
                continue
            if A[i][c] != 0:
                op = _add(A, i, r, -A[i][c])
                log_fn(f"Operación: {op}\n" + matriz_str(A))

        r += 1                        # Avanzar a la siguiente fila de pivote
        if r == m:                    # Si se acaban las filas, terminar
            break

    # Clasificación de resultados
    # Caso inconsistente: fila con todos ceros en coeficientes pero b ≠ 0
    for i in range(m):
        if all(A[i][j] == 0 for j in range(n)) and A[i][n] != 0:
            log_fn(matriz_str(A, "Matriz final (RREF)"))
            return "inconsistente", A

    # Contar filas no nulas (con pivotes) y compararlas con n
    filas_no_nulas = sum(1 for i in range(m) if any(A[i][j] != 0 for j in range(n)))
    if filas_no_nulas < n:            # Menos pivotes que variables → infinitas soluciones
        log_fn(matriz_str(A, "Matriz final (RREF)"))
        return "infinitas", A

    # Caso de solución única
    log_fn(matriz_str(A, "Matriz final (RREF)"))
    return "unica", A

# Función para extraer solución única de una matriz en RREF
def leer_solucion_unica(A):
    """ Extrae el vector [x1..xn] de una RREF consistente con un pivote por columna. """
    n = len(A[0]) - 1                 # Número de variables
    m = len(A)                        # Número de filas
    sol = [None]*n                    # Inicializar solución
    for j in range(n):                # Recorre cada columna de variable
        # Buscar fila donde hay pivote (1 en esa columna y 0 en todas las demás)
        fila = next((r for r in range(m) if A[r][j] == 1 and all(A[k][j] == 0 for k in range(m) if k != r)), None)
        if fila is not None:          # Si hay pivote, asignar valor de la columna de términos independientes
            sol[j] = A[fila][n]
    return sol                        # Devuelve la lista de soluciones
