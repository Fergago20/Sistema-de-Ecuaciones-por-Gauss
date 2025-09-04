import tkinter as tk
from tkinter import messagebox
from controller.logica import Logica

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ecuaciones")
        self.root.geometry("600x500")
        self.entries = []

        # Inputs de número de ecuaciones e incógnitas
        tk.Label(root, text="Número de ecuaciones:").pack()
        self.num_ecuaciones = tk.Entry(root)
        self.num_ecuaciones.pack()

        tk.Label(root, text="Número de incógnitas:").pack()
        self.num_incognitas = tk.Entry(root)
        self.num_incognitas.pack()

        tk.Button(root, text="Generar campos", command=self.generar_campos).pack(pady=10)

        self.campos_frame = tk.Frame(root)
        self.campos_frame.pack(pady=10)

        tk.Button(root, text="Resolver", command=self.resolver).pack(pady=10)

        self.resultado_text = tk.Text(root, height=10, width=70)
        self.resultado_text.pack(pady=10)

    def generar_campos(self):
        # Limpiar campos antiguos
        for widget in self.campos_frame.winfo_children():
            widget.destroy()
        self.entries = []

        try:
            n = int(self.num_ecuaciones.get())
            m = int(self.num_incognitas.get())
            if n <= 0 or m <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese enteros positivos para ecuaciones e incógnitas")
            return

        for i in range(n):
            fila_frame = tk.Frame(self.campos_frame)
            fila_frame.pack()
            fila_entries = []
            for j in range(m):
                e = tk.Entry(fila_frame, width=5)
                e.pack(side="left", padx=2)
                e.insert(0, "0")
                fila_entries.append(e)
            # Término independiente
            tk.Label(fila_frame, text="=").pack(side="left")
            b = tk.Entry(fila_frame, width=5)
            b.pack(side="left", padx=2)
            b.insert(0, "0")
            fila_entries.append(b)
            self.entries.append(fila_entries)

    def resolver(self):
        ecuaciones = []
        for fila in self.entries:
            fila_valores = []
            try:
                for e in fila:
                    valor = e.get()
                    if valor == "":
                        valor = 0
                    fila_valores.append(float(valor))
            except ValueError:
                messagebox.showerror("Error", "Todos los coeficientes deben ser números válidos")
                return
            ecuaciones.append(fila_valores)

        n = len(ecuaciones)
        m = len(ecuaciones[0]) - 1 if n > 0 else 0

        logica = Logica(m, n)
        logica.limpiar()

        try:
            for ecu in ecuaciones:
                logica.agregar_ecuacion(ecu)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            matriz_resuelta = logica.resolver_sistema()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al resolver: {str(e)}")
            return

        # Mostrar resultados
        self.resultado_text.delete("1.0", tk.END)
        self.resultado_text.insert(tk.END, "Matriz final:\n")
        for fila in logica.matriz.matriz:
            self.resultado_text.insert(tk.END, " | ".join(f"{x:.2f}" for x in fila) + "\n")

        self.resultado_text.insert(tk.END, "\nSoluciones:\n")
        soluciones = logica.matriz.ObtenerSoluciones()
        self.resultado_text.insert(tk.END, ", ".join(f"{x:.2f}" for x in soluciones))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
