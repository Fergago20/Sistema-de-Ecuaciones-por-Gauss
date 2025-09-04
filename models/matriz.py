from models.Ecuaciones import SistemaEcuaciones
class Matriz:
    def __init__(self, numIncognitas, numEcuaciones):
        self.sistema = SistemaEcuaciones(numIncognitas, numEcuaciones)
        self.matriz = []
    
    def AgregarEcuacion(self, ecuacion):
        self.sistema.AgregarEcuacion(ecuacion)
        self.matriz = self.sistema.ObtenerMatrizAumentada()
    
    def GaussJordan(self):
        matriz = [fila[:] for fila in self.matriz]
        numFilas = len(matriz)
        numCols = len(matriz[0])

        # Recorremos columnas hasta la penúltima (última es término independiente)
        for i in range(min(numFilas, numCols - 1)):
            # Buscar un pivote no nulo en la columna actual
            if matriz[i][i] == 0:
                fila_no_nula = None
                for k in range(i + 1, numFilas):
                    if matriz[k][i] != 0:
                        fila_no_nula = k
                        break
                if fila_no_nula is not None:
                    # Intercambiar filas
                    matriz[i], matriz[fila_no_nula] = matriz[fila_no_nula], matriz[i]
                else:
                    # No hay pivote válido, pasamos a la siguiente columna
                    continue

            pivote = matriz[i][i]
            if pivote == 0:  # Si sigue en cero, no podemos normalizar
                continue

            # Normalizar fila (pivote = 1)
            for j in range(numCols):
                matriz[i][j] /= pivote

            # Hacer ceros en la columna del pivote
            for k in range(numFilas):
                if k != i:
                    factor = matriz[k][i]
                    for j in range(numCols):
                        matriz[k][j] -= factor * matriz[i][j]

        self.matriz = matriz
        return matriz

    def ObtenerSoluciones(self):
        soluciones = [fila[-1] for fila in self.matriz]
        return soluciones
    def retornarMatriz(self):
        return self.matriz
    
    def limpiarMatriz(self):
        self.matriz = []
        self.sistema.ecuaciones = []