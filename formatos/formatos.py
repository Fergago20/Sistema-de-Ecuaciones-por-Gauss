from fractions import Fraction

#Da formato a un número (float o Fraction) para mostrarlo como entero, fracción o decimal.
def _fmt(x):
    if isinstance(x, float):
        # Si el valor es casi un entero, se muestra como tal
        if abs(x - round(x)) < 1e-12:
            return str(int(round(x)))
        # Si no, se convierte a fracción con denominador limitado
        f = Fraction(x).limit_denominator(1000)
        return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"
    if isinstance(x, Fraction):
        # Si es fracción con denominador 1, mostrar solo el numerador
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return str(x)  # Para otros tipos, se convierte a texto

#Calcula el ancho máximo (número de caracteres) que ocupa cada columna de la matriz M.
def _anchos(M):
    if not M: return []   # Si la matriz está vacía, no hay anchos
    w = [0]*len(M[0])     # Lista de anchos, uno por columna
    for F in M:           # Para cada fila F de la matriz
        for j, v in enumerate(F):
            s = _fmt(v)   # Formatear el valor
            w[j] = max(w[j], len(s))  # Guardar el ancho máximo
    return w

#Devuelve un string con la matriz M representada en texto.
def matriz_texto(M, titulo=None):
    if not M: return "(matriz vacía)\n"
    w = _anchos(M)              # Ancho de cada columna
    out = [titulo] if titulo else []  # Si hay título, se agrega al inicio
    for F in M:                 # Recorre cada fila
        # Alinea cada valor de la fila a la derecha según el ancho de su columna
        c = [_fmt(v).rjust(w[j]) for j, v in enumerate(F)]
        # Forma la fila con corchetes
        out.append("[ " + "  ".join(c) + " ]")
    return "\n".join(out) + "\n"  # Une todas las filas con saltos de línea
