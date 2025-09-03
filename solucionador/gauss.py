from fractions import Fraction
from copy import deepcopy
from .formats import matriz_str, fmt_frac

def _swap(A, i, j):
    if i != j:
        A[i], A[j] = A[j], A[i]
        return f"F{i+1} ↔ F{j+1}"

def _scale(A, i, k: Fraction):
    if k == 0:
        raise ZeroDivisionError("No se puede escalar por 0.")
    A[i] = [a * k for a in A[i]]
    return f"F{i+1} ← ({fmt_frac(k)})·F{i+1}"

def _add(A, t, s, k: Fraction):
    A[t] = [A[t][c] + k * A[s][c] for c in range(len(A[0]))]
    return f"F{t+1} ← F{t+1} + ({fmt_frac(k)})·F{s+1}"

def gauss_jordan_with_log(A_in, log_fn=lambda s: None):
    """
    Lleva A a RREF con notación de operaciones. Usa pivoteo simple (no parciales por magnitud para mantenerlo didáctico).
    Retorna: (tipo, A) donde tipo ∈ {"unica","infinitas","inconsistente"}.
    """
    A = deepcopy(A_in)
    m = len(A); n = len(A[0]) - 1

    log_fn(matriz_str(A, "Matriz inicial [A|b]"))

    r = 0
    for c in range(n):
        # Buscar pivote ≠ 0 desde r hacia abajo
        piv = None
        for i in range(r, m):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue

        op = _swap(A, r, piv)
        if op:
            log_fn(f"Operación: {op}\n" + matriz_str(A))

        val = A[r][c]
        if val != 1:
            op = _scale(A, r, Fraction(1, 1) / val)
            log_fn(f"Operación: {op}\n" + matriz_str(A))

        # ceros en toda la columna
        for i in range(m):
            if i == r:
                continue
            if A[i][c] != 0:
                op = _add(A, i, r, -A[i][c])
                log_fn(f"Operación: {op}\n" + matriz_str(A))

        r += 1
        if r == m:
            break

    # Clasificación
    # Inconsistente: fila [0 ... 0 | b!=0]
    for i in range(m):
        if all(A[i][j] == 0 for j in range(n)) and A[i][n] != 0:
            log_fn(matriz_str(A, "Matriz final (RREF)"))
            return "inconsistente", A

    # Contar filas no nulas (pivotes) vs n variables
    filas_no_nulas = sum(1 for i in range(m) if any(A[i][j] != 0 for j in range(n)))
    if filas_no_nulas < n:
        log_fn(matriz_str(A, "Matriz final (RREF)"))
        return "infinitas", A

    log_fn(matriz_str(A, "Matriz final (RREF)"))
    return "unica", A

def leer_solucion_unica(A):
    """ Extrae [x1..xn] de una RREF consistente con pivote por columna. """
    n = len(A[0]) - 1
    m = len(A)
    sol = [None]*n
    for j in range(n):
        fila = next((r for r in range(m) if A[r][j] == 1 and all(A[k][j] == 0 for k in range(m) if k != r)), None)
        if fila is not None:
            sol[j] = A[fila][n]
    return sol
