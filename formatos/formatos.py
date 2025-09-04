from fractions import Fraction  # Fracciones exactas (p/q) para impresión precisa

# Formatea un valor para impresión: entero "p" o fracción "p/q".
def _fmt(x):
    if isinstance(x, float):  # En el prototipo exacto no aceptamos floats
        raise TypeError("Prototipo exacto: Usa Fraction o int.")
    if isinstance(x, Fraction):  # Fraction -> "p" si denom=1, si no "p/q"
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return str(x)  # ints u otros tipos imprimibles

# Calcula el ancho máximo (en caracteres) de cada columna ya formateada.
def _anchos(M):
    if not M:  # Matriz vacía
        return []
    w = [0] * len(M[0])  # Un ancho por columna
    for F in M:
        for j, v in enumerate(F):
            s = _fmt(v)              # Longitud final depende del formato
            w[j] = max(w[j], len(s)) # Mantener el máximo por columna
    return w

# Construye una representación alineada de la matriz (opcionalmente con título).
def matriz_texto(M, titulo=None):
    if not M:
        return "(matriz vacía)\n"
    w = _anchos(M)                     # Ancho por columna para alinear
    out = [titulo] if titulo else []   # Primera línea: título si existe
    for F in M:
        c = [_fmt(v).rjust(w[j]) for j, v in enumerate(F)]  # Alineación a la derecha
        out.append("[ " + "  ".join(c) + " ]")              # Fila con corchetes y doble espacio
    return "\n".join(out) + "\n"       # Bloque con salto final
