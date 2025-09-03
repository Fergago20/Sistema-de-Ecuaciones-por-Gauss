from fractions import Fraction

def formatear(num, ancho=5):
    if hasattr(num, 'denominator') and num.denominator == 1:
        s = str(num.numerator)
    else:
        s = str(num)
    return s.rjust(ancho)

def mostrar_matriz(matriz, operacion=None):
    if operacion:
        print(f"\nOperación: {operacion}")
    for fila in matriz:
        fila_str = " ".join(formatear(v) for v in fila)
        print("[", fila_str, "]")
    print()

def intercambiar(matriz, i, j):
    if i != j:
        matriz[i], matriz[j] = matriz[j], matriz[i]
        return f"Fila {i+1} ↔ Fila {j+1}"
    return None

def multiplicar_fila(matriz, i, k: Fraction):
    if k == 0:
        return None
    matriz[i] = [a * k for a in matriz[i]]
    return f"Fila {i+1} ← ({formatear(k)})·Fila {i+1}"

def sumar_filas(matriz, destino, fuente, k: Fraction):
    matriz[destino] = [matriz[destino][c] + k * matriz[fuente][c] for c in range(len(matriz[0]))]
    return f"Fila {destino+1} ← Fila {destino+1} + ({formatear(k)})·Fila {fuente+1}"
