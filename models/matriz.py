from models.Ecuaciones import SistemaEcuaciones
class Matriz:
    def __init__(self, numIncognitas, numEcuaciones):
        self.sistema = SistemaEcuaciones(numIncognitas, numEcuaciones)
        self.matriz = []
    
    def AgregarEcuacion(self, ecuacion):
        self.sistema.AgregarEcuacion(ecuacion)
        self.matriz = self.sistema.ObtenerMatrizAumentada()
    
    def MostrarMatriz(self):
        self.sistema.MostrarSistema()
        print("Matriz Aumentada:")
        for fila in self.matriz:
            print(" | ".join(f"{coef:8.3f}" for coef in fila))

    

    
    def GaussJordan(self):
        matriz = [fila[:] for fila in self.matriz]
        numFilas = len(matriz)
        numCols = len(matriz[0])
        
        for i in range(numFilas):
            # Hacer el pivote 1
            pivote = matriz[i][i]
            if pivote == 0:
                for k in range(i + 1, numFilas):
                    if matriz[k][i] != 0:
                        self.cambiarFila(i, k)
                        pivote = matriz[i][i]
                        break
                if pivote == 0:
                    continue
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
    
    def cambiarFila(self, fila1, fila2):
        self.matriz[fila1], self.matriz[fila2] = self.matriz[fila2], self.matriz[fila1]
    
    def ObtenerSoluciones(self):
        soluciones = [fila[-1] for fila in self.matriz]
        return soluciones
    
    def limpiarMatriz(self):
        self.matriz = []
        self.sistema.ecuaciones = []