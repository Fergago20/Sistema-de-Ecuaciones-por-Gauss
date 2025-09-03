from models.matriz import Matriz

class Logica:
    def __init__(self, numIncognitas, numEcuaciones):
        self.matriz = Matriz(numIncognitas, numEcuaciones)
    
    def agregar_ecuacion(self, ecuacion):
        self.matriz.AgregarEcuacion(ecuacion)
    
    def mostrar_matriz(self):
        self.matriz.MostrarMatriz()
    
    def resolver_sistema(self):
        try:
            self.matriz.GaussJordan()
            soluciones = self.matriz.ObtenerSoluciones()
            return soluciones
        except ValueError as e:
            return str(e)
    
    def limpiar(self):
        self.matriz.limpiarMatriz()