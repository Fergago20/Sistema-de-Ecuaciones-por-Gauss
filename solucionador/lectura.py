from fractions import Fraction
import re

PATRON_VAR = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')

def normalizar_expresion(texto: str) -> str:
    texto = texto.replace('−', '-').replace(' ', '').replace('*', '')
    salida = []
    for i, ch in enumerate(texto):
        if ch == '-' and i != 0:
            salida.append('+-')
        else:
            salida.append(ch)
    texto = ''.join(salida)
    if texto.startswith('+'):
        texto = texto[1:]
    return texto

def leer_lado(expresion: str):
    """Devuelve (coeficientes, constante) de un lado de la ecuación."""
    expresion = normalizar_expresion(expresion)
    if expresion == '':
        return {}, Fraction(0)
    terminos = [t for t in expresion.split('+') if t != '']

    coeficientes = {}
    constante = Fraction(0)
    patron = re.compile(r'^(-)?(?:(\d+(?:/\d+)?|\d*\.\d+)?)?([A-Za-z_][A-Za-z0-9_]*)?$')
    for t in terminos:
        m = patron.match(t)
        if not m:
            raise ValueError(f"Término no reconocido: '{t}'")
        signo_str, numero_str, variable = m.groups()
        signo = -1 if signo_str else 1

        if variable:
            coef = Fraction(1) if not numero_str else Fraction(numero_str)
            coef *= signo
            coeficientes[variable] = coeficientes.get(variable, Fraction(0)) + coef
        else:
            if not numero_str:
                raise ValueError(f"Término constante inválido: '{t}'")
            constante += signo * Fraction(numero_str)
    return coeficientes, constante

def leer_ecuacion(ecuacion: str):
    if '=' not in ecuacion:
        raise ValueError("Cada ecuación debe contener '='.")
    izquierda, derecha = ecuacion.split('=', 1)
    coef_izq, cte_izq = leer_lado(izquierda)
    coef_der, cte_der = leer_lado(derecha)
    todas = set(coef_izq) | set(coef_der)
    coefs = {v: coef_izq.get(v, 0) - coef_der.get(v, 0) for v in todas}
    b = cte_der - cte_izq
    return coefs, b

def construir_matriz(ecuaciones):
    orden_vars = []
    vistos = set()
    for e in ecuaciones:
        for m in PATRON_VAR.finditer(e.replace(' ', '')):
            v = m.group(0)
            if v not in vistos:
                vistos.add(v)
                orden_vars.append(v)
    interpretadas = [leer_ecuacion(e) for e in ecuaciones]
    for coefs, _ in interpretadas:
        for v in coefs:
            if v not in vistos:
                vistos.add(v)
                orden_vars.append(v)
    n = len(orden_vars)
    matriz = []
    for coefs, b in interpretadas:
        fila = [Fraction(0) for _ in range(n+1)]
        for j, v in enumerate(orden_vars):
            fila[j] = coefs.get(v, Fraction(0))
        fila[n] = b
        matriz.append(fila)
    return orden_vars, matriz
