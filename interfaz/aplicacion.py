"""Aplicación Tkinter para construir y resolver sistemas lineales por Gauss-Jordan.

    - Permite elegir número de incógnitas (n) y ecuaciones (m).
    - Gener una grilla para ingresar coeficientes (A) y términos independientes (b).
    - Muestra la matriz aumentada inicial [A|b], la forma reducida por filas (RREF),
      y un resumen de la solucion (única/infinitas/inconsistente).
"""

import tkinter as tk
from tkinter import messagebox
from fractions import Fraction

# Funciones propias del proyecto 
from solucionador.gauss import gauss_jordan, leer_solucion_unica
from formatos.formatos import matriz_texto, _fmt


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistemas de Ecuaciones")
        self.geometry("1100x650")       # Tamaño amplio para acomodar grillas y paneles
        self.configure(bg="#111")       # Fondo oscuro

        # ----- Barra superior: controles para n (incógnitas) y m (ecuaciones) -----
        top = tk.Frame(self, bg="#111")
        top.pack(side=tk.TOP, fill=tk.X, padx=12, pady=10)

        tk.Label(top, text="Incógnitas:", fg="#ddd", bg="#111").pack(side=tk.LEFT)
        self.n = tk.IntVar(value=1)     # Valor por defecto: 1 incógnita
        tk.Spinbox(top, from_=1, to=10, width=3, textvariable=self.n).pack(side=tk.LEFT, padx=6)

        tk.Label(top, text="Ecuaciones:", fg="#ddd", bg="#111").pack(side=tk.LEFT, padx=(12, 0))
        self.m = tk.IntVar(value=2)     # Valor por defecto: 2 ecuaciones
        # Mínimo 2 ecuaciones; máximo 12
        tk.Spinbox(top, from_=2, to=12, width=3, textvariable=self.m).pack(side=tk.LEFT, padx=6)

        # Botón para (re)generar la grilla de entradas según n y m
        tk.Button(top, text="Generar", command=self.generar).pack(side=tk.LEFT, padx=10)

        # ----- Columna izquierda: grilla de entradas + botones + salida de solución -----
        left = tk.Frame(self, bg="#111")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=12, pady=12)

        # Contenedor de la grilla [A|b]
        self.grid = tk.Frame(left, bg="#111")
        self.grid.pack(anchor="w")

        # Botones de acción
        btns = tk.Frame(left, bg="#111")
        btns.pack(anchor="w", pady=10)
        tk.Button(btns, text="Resolver", command=self.resolver).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Limpiar", command=self.limpiar).grid(row=0, column=1, padx=5)

        # Caja de texto para mostrar la solución legible
        tk.Label(left, text="Solución:", fg="#ddd", bg="#111").pack(anchor="w", pady=(8, 2))
        self.txt_sol = tk.Text(left, width=48, height=10)
        self.txt_sol.pack(anchor="w")

        # ----- Columna derecha: resumen/bitácora grande (matrices y pasos) -----
        right = tk.Frame(self, bg="#111")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)

        tk.Label(right, text="Resumen:", fg="#ddd", bg="#111").pack(anchor="w")
        # wrap="word" para no cortar palabras; Consolas para alinear columnas de matrices
        self.txt = tk.Text(right, wrap="word", font=("Consolas", 11))
        self.txt.pack(fill=tk.BOTH, expand=True)

        # Estructuras que guardan referencias a las entradas (Entry) de coeficientes y b
        self.E, self.B = [], []

        # Genera la grilla inicial con los valores por defecto (n=1, m=2)
        self.generar()

    # ---------- Utilidades internas ----------

    @staticmethod
    def _num(s: str) -> float:
        """Convierte el texto de una celda a número (float).
        - Acepta fracciones tipo '3/4' usando Fraction.
        - Cadena vacía -> 0.0
        """
        s = (s or "").strip()
        if not s:
            return 0.0
        # Si la celda contiene '/', se interpreta como fracción exacta
        return float(Fraction(s)) if "/" in s else float(s)

    def _matriz(self):
        """Construye la matriz aumentada [A|b] leyendo las entradas de la grilla."""
        m, n = len(self.E), (len(self.E[0]) if self.E else 0)
        A0 = []
        for i in range(m):
            # Lee coeficientes de la fila i
            fila = [self._num(self.E[i][j].get()) for j in range(n)]
            # Agrega el término independiente b_i al final de la fila
            fila.append(self._num(self.B[i].get()))
            A0.append(fila)
        return A0

    # ---------- Acciones de UI ----------

    def generar(self):
        """Crea/renueva la grilla de entradas según n (incógnitas) y m (ecuaciones)."""
        # Borra widgets previos si se regenera
        for w in self.grid.winfo_children():
            w.destroy()
        self.E.clear()
        self.B.clear()

        n, m = self.n.get(), self.m.get()

        # Encabezados de columnas: x1..xn y la columna '=' para b
        for j in range(n):
            tk.Label(self.grid, text=f"x{j+1}", fg="#ddd", bg="#111").grid(row=0, column=j, padx=4)
        tk.Label(self.grid, text="=", fg="#ddd", bg="#111").grid(row=0, column=n, padx=8)

        # Crea las entradas para coeficientes A[i][j] y para b[i]
        for i in range(m):
            fila = []
            for j in range(n):
                e = tk.Entry(self.grid, width=7)
                e.grid(row=i + 1, column=j, padx=4, pady=4)
                e.insert(0, "0")  # valor inicial 0
                fila.append(e)
            self.E.append(fila)

            # Entrada para el término independiente b_i
            eb = tk.Entry(self.grid, width=7)
            eb.grid(row=i + 1, column=n, padx=8, pady=4)
            eb.insert(0, "0")  # valor inicial 0
            self.B.append(eb)

    def limpiar(self):
        """Resetea todas las entradas a 0 y limpia las salidas de texto."""
        for fila in self.E:
            for e in fila:
                e.delete(0, tk.END)
                e.insert(0, "0")
        for eb in self.B:
            eb.delete(0, tk.END)
            eb.insert(0, "0")
        self.txt.delete("1.0", tk.END)      # limpia resumen
        self.txt_sol.delete("1.0", tk.END)  # limpia solución

    def resolver(self):
        """Ejecuta Gauss-Jordan y muestra:
        - Matriz aumentada inicial [A|b]
        - Matriz reducida por filas (RREF)
        - Tipo de sistema y su(s) solución(es)
        """
        if not self.E:
            messagebox.showwarning("Aviso", "Genera la grilla primero.")
            return

        # Limpia las salidas antes de resolver
        self.txt.delete("1.0", tk.END)
        self.txt_sol.delete("1.0", tk.END)

        # Intenta leer y convertir la grilla a números
        try:
            A0 = self._matriz()
        except Exception as e:
            messagebox.showerror("Error", f"Revisa los números.\n{e}")
            return

        # Muestra matriz inicial y, luego de Gauss-Jordan, la matriz final (RREF)
        self.txt.insert(tk.END, matriz_texto(A0, "Matriz inicial [A|b]"))
        tipo, A = gauss_jordan(A0)
        self.txt.insert(tk.END, matriz_texto(A, "Matriz final (RREF)"))

        # Determina el tipo de sistema y refleja el resultado
        if tipo == "inconsistente":
            self.txt_sol.insert(tk.END, "El sistema no tiene solución.\n")
            return
        if tipo == "infinitas":
            self.txt_sol.insert(tk.END, "El sistema tiene infinitas soluciones.\n")
            return

        # Caso de solución única: intenta leerla en formato amigable
        sol = leer_solucion_unica(A)
        if any(v is not None for v in sol):
            self.txt_sol.insert(tk.END, "Solución única:\n")
            for j, v in enumerate(sol, 1):
                if v is not None:
                    self.txt_sol.insert(tk.END, f"  x{j} = {_fmt(v)}\n")
        else:
            # Respaldo: toma los valores de la última columna de A (si aplica)
            n = len(A[0]) - 1
            self.txt_sol.insert(tk.END, "Solución única (por columnas):\n")
            for j in range(n):
                self.txt_sol.insert(tk.END, f"  x{j+1} = {_fmt(A[j][-1])}\n")


def iniciar_aplicacion():
    """Punto de entrada para lanzar la interfaz."""
    App().mainloop()
