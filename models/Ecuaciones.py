class SistemaEcuaciones:
    def __init__(self, numIncognitas, numEcuaciones):
        self.numIncognitas = numIncognitas
        self.numEcuaciones = numEcuaciones
        self.ecuaciones = []
    
    def AgregarEcuacion(self, ecuacion):
        if len(ecuacion) != self.numIncognitas + 1:
            raise ValueError("La ecuación debe tener el número correcto de coeficientes más el término independiente.")
        if len(self.ecuaciones) > self.numEcuaciones:
            raise ValueError("Se ha excedido el número de ecuaciones permitidas.")
        self.ecuaciones.append(ecuacion)
    
    def ObtenerMatrizAumentada(self):
        return [ecuacion[:] for ecuacion in self.ecuaciones]