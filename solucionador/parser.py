from fractions import Fraction
import re

VAR_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')

def _norm_expr(s: str) -> str:
    s = s.replace('−', '-').replace(' ', '').replace('*', '')
    out = []
    for i, ch in enumerate(s):
        if ch == '-' and i != 0:
            out.append('+-')
        else:
            out.append(ch)
    s = ''.join(out)
    if s.startswith('+'):
        s = s[1:]
    return s

def _parse_side(expr: str):
    expr = _norm_expr(expr)

    # Si el lado queda vacío, lo tratamos como 0 (p. ej. "= 2" deja el lado izquierdo vacío)
    if expr == '':
        return {}, Fraction(0)

    # Detectar operadores colgando al final: "x +", "x -"
    # Tras normalizar, un '-' interno se convierte en '+-'; si el usuario dejó un '+' o un '-' al final,
    # lo veremos como expr.endswith('+') o expr.endswith('+-')
    if expr.endswith('+') or expr.endswith('+-'):
        raise ValueError("Expresión incompleta: falta término junto a '+' o '-'.")

    # No ocultar vacíos: si hay '++' o '+-+' terminará generando tokens vacíos; eso es error
    parts = expr.split('+')
    coeffs = {}
    const = Fraction(0)
    pat = re.compile(r'^(-)?(?:(\d+(?:/\d+)?|\d*\.\d+)?)?([A-Za-z_][A-Za-z0-9_]*)?$')

    for tok in parts:
        if tok == '':
            # Esto ocurre con patrones como "x++y" o "x+" (ya cubierto arriba) → inválido
            raise ValueError("Expresión incompleta o con operadores consecutivos.")

        m = pat.match(tok)
        if not m:
            # Aquí caen cosas como "@y", "x#2", etc.
            raise ValueError(f"Término no reconocido: '{tok}'")

        sign_str, num_str, var = m.groups()
        sign = -1 if sign_str else 1

        if var:
            # término con variable: coef 1 por defecto
            coef = Fraction(1) if not num_str else Fraction(num_str)
            coef *= sign
            coeffs[var] = coeffs.get(var, Fraction(0)) + coef
        else:
            # término constante puro (sin variable) debe traer número
            if not num_str:
                # Ejemplos: solo '-' o nada → inválido (como "x + = 2")
                raise ValueError(f"Término constante inválido: '{tok}'")
            const += sign * Fraction(num_str)

    return coeffs, const

def parse_equation(eq: str):
    if '=' not in eq:
        raise ValueError("Cada ecuación debe contener '='.")
    lhs, rhs = eq.split('=', 1)
    lc, lcst = _parse_side(lhs)
    rc, rcst = _parse_side(rhs)
    allv = set(lc) | set(rc)
    coefs = {v: lc.get(v, 0) - rc.get(v, 0) for v in allv}
    b = rcst - lcst
    return coefs, b

def construir_matriz(equations: list[str]):
    # Orden de variables por primera aparición textual
    var_order = []
    seen = set()
    for e in equations:
        for m in VAR_RE.finditer(e.replace(' ', '')):
            v = m.group(0)
            if v not in seen:
                seen.add(v)
                var_order.append(v)

    parsed = [parse_equation(e) for e in equations]
    # Por si aparecieron variables solo tras mover términos
    for coefs, _ in parsed:
        for v in coefs:
            if v not in seen:
                seen.add(v)
                var_order.append(v)

    n = len(var_order)
    A = []
    for coefs, b in parsed:
        row = [Fraction(0) for _ in range(n+1)]
        for j, v in enumerate(var_order):
            row[j] = coefs.get(v, Fraction(0))
        row[n] = b
        A.append(row)
    return var_order, A
