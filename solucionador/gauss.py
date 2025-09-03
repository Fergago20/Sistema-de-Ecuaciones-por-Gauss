from fractions import Fraction
from .operaciones import mostrar_matriz, intercambiar, multiplicar_fila, sumar_filas

def metodo_gauss_jordan(matriz):
    filas = len(matriz)
    columnas = len(matriz[0]) - 1
    r = 0
    for c in range(columnas):
        pivote = None
        for i in range(r, filas):
            if matriz[i][c] != 0:
                pivote = i
                break
        if pivote is None:
            continue

        op = intercambiar(matriz, r, pivote)
        if op: mostrar_matriz(matriz, op)

        val = matriz[r][c]
        if val != 1:
            op = multiplicar_fila(matriz, r, Fraction(1, 1) / val)
            if op: mostrar_matriz(matriz, op)

        for i in range(filas):
            if i == r:
                continue
            if matriz[i][c] != 0:
                op = sumar_filas(matriz, i, r, -matriz[i][c])
                if op: mostrar_matriz(matriz, op)

        r += 1
        if r == filas:
            break

    for i in range(filas):
        if all(matriz[i][j] == 0 for j in range(columnas)) and matriz[i][columnas] != 0:
            print("El sistema no tiene solución.")
            return False
    return True
