from fractions import Fraction

def fmt_frac(x: Fraction) -> str:
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"
    return str(x)

def _col_widths(mat):
    if not mat:
        return []
    cols = len(mat[0])
    w = [0]*cols
    for row in mat:
        for j, val in enumerate(row):
            s = fmt_frac(val)
            w[j] = max(w[j], len(s))
    return w

def matriz_str(mat, titulo=None):
    if not mat:
        return "(matriz vacía)\n"
    widths = _col_widths(mat)
    out = []
    if titulo:
        out.append(titulo)
    for row in mat:
        cells = [fmt_frac(val).rjust(widths[j]) for j, val in enumerate(row)]
        out.append("[ " + "  ".join(cells) + " ]")
    return "\n".join(out) + "\n"
