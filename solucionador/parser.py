from fractions import Fraction   # Para manejar fracciones exactas
import re                       # Para trabajar con expresiones regulares

# Expresión regular para identificar variables válidas (ej: x, y1, var_2)
VAR_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')

# Normaliza una expresión para que sea más fácil de procesar
def _norm_expr(s: str) -> str:
    s = s.replace('−', '-')      # Reemplaza guiones largos por '-'
    s = s.replace(' ', '')       # Elimina espacios
    s = s.replace('*', '')       # Elimina el símbolo de multiplicación (implícito en álgebra)

    out = []
    for i, ch in enumerate(s):
        # Reemplaza "-" interno por "+-" (para poder separar términos después con split)
        if ch == '-' and i != 0:
            out.append('+-')
        else:
            out.append(ch)
    s = ''.join(out)

    # Si la expresión empieza con "+", lo quitamos
    if s.startswith('+'):
        s = s[1:]
    return s

# Parsea un lado de la ecuación (izquierdo o derecho)
def _parse_side(expr: str):
    expr = _norm_expr(expr)

    # Si el lado queda vacío, lo tratamos como 0 (ej: "= 2" → lado izquierdo vacío)
    if expr == '':
        return {}, Fraction(0)

    # Detectar expresiones incompletas como "x +" o "x -"
    if expr.endswith('+') or expr.endswith('+-'):
        raise ValueError("Expresión incompleta: falta término junto a '+' o '-'.")

    # Dividir la expresión en términos (separados por "+")
    parts = expr.split('+')
    coeffs = {}                  # Diccionario de coeficientes por variable
    const = Fraction(0)          # Constante independiente

    # Patrón para reconocer términos válidos: signo, número, variable
    pat = re.compile(r'^(-)?(?:(\d+(?:/\d+)?|\d*\.\d+)?)?([A-Za-z_][A-Za-z0-9_]*)?$')

    for tok in parts:
        if tok == '':
            # Ejemplo: "x++y" o "x+" → error
            raise ValueError("Expresión incompleta o con operadores consecutivos.")

        m = pat.match(tok)
        if not m:
            # Si el término no coincide con el patrón, es inválido
            raise ValueError(f"Término no reconocido: '{tok}'")

        sign_str, num_str, var = m.groups()    # Extraer signo, número, variable
        sign = -1 if sign_str else 1           # Si hay '-', signo = -1, sino = +1

        if var:
            # Es un término con variable (ej: "2x", "-y")
            coef = Fraction(1) if not num_str else Fraction(num_str)  # Coef por defecto = 1
            coef *= sign
            coeffs[var] = coeffs.get(var, Fraction(0)) + coef
        else:
            # Es un término constante puro (sin variable)
            if not num_str:
                raise ValueError(f"Término constante inválido: '{tok}'")
            const += sign * Fraction(num_str)

    return coeffs, const

# Convierte una ecuación en coeficientes y término independiente
def analizar_ecuacion(eq: str):
    if '=' not in eq:
        raise ValueError("Cada ecuación debe contener '='.")

    lhs, rhs = eq.split('=', 1)   # Separar lado izquierdo y derecho
    lc, lcst = _parse_side(lhs)   # Coeficientes y constante del lado izquierdo
    rc, rcst = _parse_side(rhs)   # Coeficientes y constante del lado derecho

    # Variables presentes en ambos lados
    allv = set(lc) | set(rc)

    # Construir diccionario con coeficientes trasladando todo al lado izquierdo
    coefs = {v: lc.get(v, 0) - rc.get(v, 0) for v in allv}

    # Término independiente (lado derecho - lado izquierdo)
    b = rcst - lcst

    return coefs, b

# Construye la matriz aumentada [A|b] a partir de un sistema de ecuaciones
def construir_matriz(equations: list[str]):
    # Detectar variables en orden de aparición
    var_order = []
    seen = set()
    for e in equations:
        for m in VAR_RE.finditer(e.replace(' ', '')):
            v = m.group(0)
            if v not in seen:
                seen.add(v)
                var_order.append(v)

    # Parsear cada ecuación en coeficientes y término independiente
    parsed = [analizar_ecuacion(e) for e in equations]

    # Asegurar que se incluyan variables que aparezcan tras mover términos
    for coefs, _ in parsed:
        for v in coefs:
            if v not in seen:
                seen.add(v)
                var_order.append(v)

    n = len(var_order)  # Número de variables
    A = []              # Matriz aumentada
    for coefs, b in parsed:
        row = [Fraction(0) for _ in range(n+1)]  # Inicializar fila con ceros
        for j, v in enumerate(var_order):
            row[j] = coefs.get(v, Fraction(0))   # Asignar coeficiente de la variable
        row[n] = b                               # Última columna es término independiente
        A.append(row)

    return var_order, A  # Devuelve el orden de variables y la matriz aumentada
