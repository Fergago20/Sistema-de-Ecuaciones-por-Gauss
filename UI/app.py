import tkinter as tk
from tkinter import messagebox
from solucionador.parser import construir_matriz, parse_equation
from solucionador.gauss import gauss_jordan_with_log, leer_solucion_unica
from solucionador.formats import matriz_str, fmt_frac

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resolución de Sistemas de Ecuaciones")
        self.geometry("1000x650")
        self.configure(bg="#111")

        # ---- Entrada de ecuación y lista
        frm_left = tk.Frame(self, bg="#111")
        frm_left.pack(side=tk.LEFT, fill=tk.Y, padx=12, pady=12)

        tk.Label(frm_left, text="Ecuación:", fg="#ddd", bg="#111").pack(anchor="w")
        self.ent_eq = tk.Entry(frm_left, width=35)
        self.ent_eq.pack(anchor="w")
        tk.Button(frm_left, text="Agregar", command=self.agregar).pack(anchor="w", pady=(6,10))

        tk.Label(frm_left, text="Sistema de ecuaciones:", fg="#ddd", bg="#111").pack(anchor="w")
        self.lst = tk.Listbox(frm_left, width=40, height=12)
        self.lst.pack(anchor="w")

        btns = tk.Frame(frm_left, bg="#111")
        btns.pack(anchor="w", pady=8)
        tk.Button(btns, text="Quitar", command=self.quitar).grid(row=0, column=0, padx=3)
        tk.Button(btns, text="Limpiar", command=self.limpiar).grid(row=0, column=1, padx=3)
        tk.Button(btns, text="Ver matriz", command=self.ver_matriz).grid(row=0, column=2, padx=3)
        tk.Button(btns, text="Resolver", command=self.resolver).grid(row=0, column=3, padx=3)

        tk.Label(frm_left, text="Solución:", fg="#ddd", bg="#111").pack(anchor="w", pady=(10,0))
        self.txt_sol = tk.Text(frm_left, width=40, height=8)
        self.txt_sol.pack(anchor="w")

        # ---- Procedimiento a la derecha
        frm_right = tk.Frame(self, bg="#111")
        frm_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)
        tk.Label(frm_right, text="Procedimiento:", fg="#ddd", bg="#111").pack(anchor="w")
        # fuente monoespaciada para alinear matrices
        self.txt_proc = tk.Text(frm_right, wrap="word", font=("Consolas", 11))
        self.txt_proc.pack(fill=tk.BOTH, expand=True)

    # ------ acciones UI
    def agregar(self):
        s = self.ent_eq.get().strip()
        if not s:
            messagebox.showwarning("Aviso", "Escribe una ecuación.")
            self.ent_eq.delete(0, tk.END)
            self.ent_eq.focus_set()
            return

        if "=" not in s:
            messagebox.showerror("Error", "La ecuación debe contener '='.")
            self.ent_eq.delete(0, tk.END)
            self.ent_eq.focus_set()
            return

        # Validación semántica con el parser ANTES de agregarla a la lista
        try:
            parse_equation(s)  # si hay error, lanzará ValueError con el mensaje correcto
        except Exception as e:
            messagebox.showerror("Error al interpretar", str(e))
            self.ent_eq.delete(0, tk.END)
            self.ent_eq.focus_set()
            return

        # Si todo OK, ahora sí agregar
        self.lst.insert(tk.END, s)
        self.ent_eq.delete(0, tk.END)
        self.ent_eq.focus_set()

    def quitar(self):
        sel = self.lst.curselection()
        if not sel:
            return
        self.lst.delete(sel[0])

    def limpiar(self):
        self.lst.delete(0, tk.END)
        self.txt_proc.delete("1.0", tk.END)
        self.txt_sol.delete("1.0", tk.END)
        self.ent_eq.delete(0, tk.END)
        self.ent_eq.focus_set()

    def _ecuaciones(self):
        return [self.lst.get(i) for i in range(self.lst.size())]

    def ver_matriz(self):
        eqs = self._ecuaciones()
        if not eqs:
            messagebox.showwarning("Aviso", "Agrega al menos una ecuación.")
            return

        # Bloquear vista de matriz si solo hay 1 ecuación (opcional)
        if len(eqs) < 2:
            messagebox.showwarning(
                "Aviso",
                "Se necesitan al menos 2 ecuaciones para formar un sistema."
            )
            return

        try:
            _, A = construir_matriz(eqs)
        except Exception as e:
            messagebox.showerror("Error al interpretar", str(e))
            return
        self.txt_proc.delete("1.0", tk.END)
        self.txt_proc.insert(tk.END, matriz_str(A, "Matriz aumentada [A|b]"))

    def resolver(self):
        eqs = self._ecuaciones()
        if not eqs:
            messagebox.showwarning("Aviso", "Agrega al menos una ecuación.")
            return

        # Validación: al menos 2 ecuaciones para que sea sistema
        if len(eqs) < 2:
            messagebox.showwarning(
                "Aviso",
                "Se necesitan al menos 2 ecuaciones para formar un sistema."
            )
            return

        self.txt_proc.delete("1.0", tk.END)
        self.txt_sol.delete("1.0", tk.END)

        # Construir matriz antes de resolver (define var_order y A0)
        try:
            var_order, A0 = construir_matriz(eqs)
        except Exception as e:
            messagebox.showerror("Error al interpretar ecuaciones", str(e))
            return

        def logger(msg: str):
            self.txt_proc.insert(tk.END, msg + "\n")

        # Resolver con logging matricial
        tipo, A = gauss_jordan_with_log(A0, logger)

        if tipo == "inconsistente":
            self.txt_sol.insert(tk.END, "no tiene solución\n")
            return

        if tipo == "infinitas":
            self.txt_sol.insert(tk.END, "tiene infinitas soluciones (dependiente)\n")
            return

        # única
        sol = leer_solucion_unica(A)
        if sol:
            self.txt_sol.insert(tk.END, "Solución única:\n")
            for name, val in zip(var_order, sol):
                if val is not None:
                    self.txt_sol.insert(tk.END, f"  {name} = {fmt_frac(val)}\n")
        else:
            # Respaldo por columnas si no se pudo mapear
            self.txt_sol.insert(tk.END, "Solución única (por columnas):\n")
            n = len(A[0]) - 1
            for j in range(n):
                self.txt_sol.insert(tk.END, f"  x{j+1} = {fmt_frac(A[j][-1])}\n")

def iniciar_app():
    App().mainloop()
