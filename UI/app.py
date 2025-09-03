import tkinter as tk
from tkinter import messagebox
# Importa funciones personalizadas del solucionador
from solucionador.parser import construir_matriz, analizar_ecuacion
from solucionador.gauss import gauss_jordan_con_log, leer_solucion_unica
from solucionador.formats import matriz_str, formatear_fraccion

# Clase principal de la aplicación (hereda de Tk)
class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resolución de Sistemas de Ecuaciones")   # Título de la ventana
        self.geometry("1000x650")                           # Tamaño inicial
        self.configure(bg="#111")                           # Fondo oscuro

        # ---- Sección izquierda: entrada de ecuaciones y botones ----
        frm_izq = tk.Frame(self, bg="#111")
        frm_izq.pack(side=tk.LEFT, fill=tk.Y, padx=12, pady=12)

        # Entrada de una ecuación
        tk.Label(frm_izq, text="Ecuación:", fg="#ddd", bg="#111").pack(anchor="w")
        self.entrada_ecuacion = tk.Entry(frm_izq, width=35)          # Campo para escribir ecuación
        self.entrada_ecuacion.pack(anchor="w")
        tk.Button(frm_izq, text="Agregar", command=self.agregar).pack(anchor="w", pady=(6,10))

        # Lista con el sistema completo
        tk.Label(frm_izq, text="Sistema de ecuaciones:", fg="#ddd", bg="#111").pack(anchor="w")
        self.lista_ecuaciones = tk.Listbox(frm_izq, width=40, height=12)  # Lista de ecuaciones
        self.lista_ecuaciones.pack(anchor="w")

        # Botones para gestionar lista
        frm_botones = tk.Frame(frm_izq, bg="#111")
        frm_botones.pack(anchor="w", pady=8)
        tk.Button(frm_botones, text="Quitar", command=self.quitar).grid(row=0, column=0, padx=3)
        tk.Button(frm_botones, text="Limpiar", command=self.limpiar).grid(row=0, column=1, padx=3)
        tk.Button(frm_botones, text="Ver matriz", command=self.ver_matriz).grid(row=0, column=2, padx=3)
        tk.Button(frm_botones, text="Resolver", command=self.resolver).grid(row=0, column=3, padx=3)

        # Área de texto para mostrar solución
        tk.Label(frm_izq, text="Solución:", fg="#ddd", bg="#111").pack(anchor="w", pady=(10,0))
        self.txt_solucion = tk.Text(frm_izq, width=40, height=8)
        self.txt_solucion.pack(anchor="w")

        # ---- Sección derecha: procedimiento paso a paso ----
        frm_der = tk.Frame(self, bg="#111")
        frm_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)
        tk.Label(frm_der, text="Procedimiento:", fg="#ddd", bg="#111").pack(anchor="w")

        # Caja de texto con fuente monoespaciada para alinear matrices
        self.txt_procedimiento = tk.Text(frm_der, wrap="word", font=("Consolas", 11))
        self.txt_procedimiento.pack(fill=tk.BOTH, expand=True)

    # ------ Métodos para acciones de la interfaz ------

    # Agregar ecuación a la lista
    def agregar(self):
        s = self.entrada_ecuacion.get().strip()
        if not s:
            messagebox.showwarning("Aviso", "Escribe una ecuación.")
            self.entrada_ecuacion.delete(0, tk.END)
            self.entrada_ecuacion.focus_set()
            return

        if "=" not in s:   # Validar que tenga '='
            messagebox.showerror("Error", "La ecuación debe contener '='.")
            self.entrada_ecuacion.delete(0, tk.END)
            self.entrada_ecuacion.focus_set()
            return

        # Validación semántica (usar parser antes de agregar)
        try:
            analizar_ecuacion(s)  # Lanza error si la ecuación es inválida
        except Exception as e:
            messagebox.showerror("Error al interpretar", str(e))
            self.entrada_ecuacion.delete(0, tk.END)
            self.entrada_ecuacion.focus_set()
            return

        # Si todo está correcto, agregar a la lista
        self.lista_ecuaciones.insert(tk.END, s)
        self.entrada_ecuacion.delete(0, tk.END)
        self.entrada_ecuacion.focus_set()

    # Quitar ecuación seleccionada
    def quitar(self):
        sel = self.lista_ecuaciones.curselection()
        if not sel:
            return
        self.lista_ecuaciones.delete(sel[0])

    # Limpiar todo (lista, soluciones, procedimiento, entrada)
    def limpiar(self):
        self.lista_ecuaciones.delete(0, tk.END)
        self.txt_procedimiento.delete("1.0", tk.END)
        self.txt_solucion.delete("1.0", tk.END)
        self.entrada_ecuacion.delete(0, tk.END)
        self.entrada_ecuacion.focus_set()

    # Devuelve lista de ecuaciones actuales
    def _ecuaciones(self):
        return [self.lista_ecuaciones.get(i) for i in range(self.lista_ecuaciones.size())]

    # Ver la matriz aumentada [A|b]
    def ver_matriz(self):
        eqs = self._ecuaciones()
        if not eqs:
            messagebox.showwarning("Aviso", "Agrega al menos una ecuación.")
            return

        if len(eqs) < 2:  # Validar que haya un sistema real
            messagebox.showwarning(
                "Aviso",
                "Se necesitan al menos 2 ecuaciones para formar un sistema."
            )
            return

        try:
            _, A = construir_matriz(eqs)  # Construir matriz aumentada
        except Exception as e:
            messagebox.showerror("Error al interpretar", str(e))
            return

        self.txt_procedimiento.delete("1.0", tk.END)
        self.txt_procedimiento.insert(tk.END, matriz_str(A, "Matriz aumentada [A|b]"))

    # Resolver el sistema de ecuaciones
    def resolver(self):
        eqs = self._ecuaciones()
        if not eqs:
            messagebox.showwarning("Aviso", "Agrega al menos una ecuación.")
            return

        if len(eqs) < 2:
            messagebox.showwarning(
                "Aviso",
                "Se necesitan al menos 2 ecuaciones para formar un sistema."
            )
            return

        # Limpiar áreas de salida
        self.txt_procedimiento.delete("1.0", tk.END)
        self.txt_solucion.delete("1.0", tk.END)

        # Construir matriz
        try:
            var_order, A0 = construir_matriz(eqs)
        except Exception as e:
            messagebox.showerror("Error al interpretar ecuaciones", str(e))
            return

        # anotar_paso interno: escribe pasos en el cuadro de procedimiento
        def anotar_paso(mensaje: str):
            self.txt_procedimiento.insert(tk.END, mensaje + "\n")

        # Resolver usando Gauss-Jordan
        tipo, A = gauss_jordan_con_log(A0, anotar_paso)

        # Revisar casos posibles
        if tipo == "inconsistente":
            self.txt_solucion.insert(tk.END, "no tiene solución\n")
            return

        if tipo == "infinitas":
            self.txt_solucion.insert(tk.END, "tiene infinitas soluciones (dependiente)\n")
            return

        # Caso: solución única
        sol = leer_solucion_unica(A)
        if sol:
            self.txt_solucion.insert(tk.END, "Solución única:\n")
            for name, val in zip(var_order, sol):
                if val is not None:
                    self.txt_solucion.insert(tk.END, f"  {name} = {formatear_fraccion(val)}\n")
        else:
            # Respaldo: mostrar resultados por columnas
            self.txt_solucion.insert(tk.END, "Solución única (por columnas):\n")
            n = len(A[0]) - 1
            for j in range(n):
                self.txt_solucion.insert(tk.END, f"  x{j+1} = {formatear_fraccion(A[j][-1])}\n")

# Función para iniciar la VentanaPrincipal
def iniciar_VentanaPrincipal():
    VentanaPrincipal().mainloop()
