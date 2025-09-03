import os
from solucionador.lectura import construir_matriz
from solucionador.operaciones import mostrar_matriz, formatear
from solucionador.gauss import metodo_gauss_jordan

def resolver_sistema():
    print("=== Resolver Sistema de Ecuaciones con Gauss-Jordan ===")
    while True:
        try:
            m = int(input("\nm (número de ecuaciones): ").strip())
            if m <= 0:
                print("Debe ser un número positivo.")
                continue
            break
        except:
            print("Entrada no válida. Intente otra vez.")

    ecuaciones = []
    for i in range(m):
        while True:
            s = input(f"Ecuación {i+1}: ").strip()
            if '=' not in s:
                print("Debe contener '='.")
                continue
            ecuaciones.append(s)
            break

    try:
        variables, matriz = construir_matriz(ecuaciones)
    except Exception as e:
        print("Error al interpretar ecuaciones:", e)
        return

    mostrar_matriz(matriz, "Matriz inicial")
    es_consistente = metodo_gauss_jordan(matriz)
    if not es_consistente:
        return

    mostrar_matriz(matriz, "Matriz final (RREF)")

    n = len(matriz[0]) - 1
    m = len(matriz)

    filas_no_nulas = sum(1 for i in range(m) if any(matriz[i][j] != 0 for j in range(n)))

    if filas_no_nulas < n:
        print("El sistema tiene infinitas soluciones (dependiente).")
        return

    print("Solución única encontrada:")
    for j in range(n):
        fila_con_pivote = next(
            (r for r in range(m) if matriz[r][j] == 1 and all(matriz[k][j] == 0 for k in range(m) if k != r)),
            None
        )
        if fila_con_pivote is not None:
            print(f"{variables[j]} = {formatear(matriz[fila_con_pivote][n])}")

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        resolver_sistema()
        otra = input("\n¿Quieres resolver otro sistema? (s/n): ").strip().lower()
        if otra != "s":
            print("Programa terminado.")
            break

if __name__ == "__main__":
    main()
