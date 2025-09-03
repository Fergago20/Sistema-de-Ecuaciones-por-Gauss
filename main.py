import tkinter as tk
from tkinter import ttk, messagebox
from controller.logica import Logica  # usa tu clase Logica

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resolución de Sistemas de Ecuaciones")
        self.configure(bg="#1a1a1a")
        self.geometry("900x600")

        self.numIncognitas = tk.IntVar(value=2)
        self.numEcuaciones = tk.IntVar(value=2)

        self.inputs = []  # guardará las filas de Entry
        self.logica = None

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Panel superior
        frame_config = tk.Frame(self, bg="#1a1a1a")
        frame_config.pack(pady=10)

        tk.Label(frame_config, text="Número de incógnitas:", fg="white", bg="#1a1a1a").grid(row=0, column=0, padx=5)
        tk.Spinbox(frame_config, from_=2, to=10, textvariable=self.numIncognitas, width=5).grid(row=0, column=1)

        tk.Label(frame_config, text="Número de ecuaciones:", fg="white", bg="#1a1a1a").grid(row=0, column=2, padx=5)
        tk.Spinbox(frame_config, from_=2, to=10, textvariable=self.numEcuaciones, width=5).grid(row=0, column=3)

        tk.Button(frame_config, text="Generar", bg="#800020", fg="white", command=self.generar_campos).grid(row=0, column=4, padx=10)

        # Panel ecuaciones
        self.frame_ecuaciones = tk.Frame(self, bg="#1a1a1a")
        self.frame_ecuaciones.pack(pady=10)

        # Panel botones
        frame_botones = tk.Frame(self, bg="#1a1a1a")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Resolver", bg="#800020", fg="white", command=self.resolver).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones, text="Limpiar", bg="#333333", fg="white", command=self.limpiar).grid(row=0, column=1, padx=10)

        # Panel resultados
        self.frame_resultados = tk.Frame(self, bg="#1a1a1a")
        self.frame_resultados.pack(fill="both", expand=True, pady=10)

        self.text_resultados = tk.Text(self.frame_resultados, bg="#262626", fg="white", height=15, wrap="word")
        self.text_resultados.pack(fill="both", expand=True, padx=10, pady=10)

    def generar_campos(self):
        for widget in self.frame_ecuaciones.winfo_children():
            widget.destroy()
        self.inputs.clear()

        n = self.numEcuaciones.get()
        m = self.numIncognitas.get()

        self.logica = Logica(m, n)

        for i in range(n):
            fila_entries = []
            for j in range(m):
                tk.Label(self.frame_ecuaciones, text=f"x{j+1}", fg="white", bg="#1a1a1a").grid(row=i, column=2*j)
                e = tk.Entry(self.frame_ecuaciones, width=5, bg="#333333", fg="white", justify="center")
                e.grid(row=i, column=2*j+1, padx=5, pady=2)
                fila_entries.append(e)

            tk.Label(self.frame_ecuaciones, text="=", fg="white", bg="#1a1a1a").grid(row=i, column=2*m)
            e_ind = tk.Entry(self.frame_ecuaciones, width=5, bg="#333333", fg="white", justify="center")
            e_ind.grid(row=i, column=2*m+1, padx=5, pady=2)
            fila_entries.append(e_ind)

            self.inputs.append(fila_entries)

    def resolver(self):
        if not self.inputs:
            messagebox.showwarning("Atención", "Primero genera los campos para las ecuaciones.")
            return

        try:
            # Leer ecuaciones
            for fila in self.inputs:
                ecuacion = [float(e.get()) if e.get() else 0.0 for e in fila]
                self.logica.agregar_ecuacion(ecuacion)

            # Resolver
            soluciones = self.logica.resolver_sistema()
            if isinstance(soluciones, str):
                self.text_resultados.delete("1.0", tk.END)
                self.text_resultados.insert(tk.END, f"Error: {soluciones}")
            else:
                matriz = self.logica.matriz.matriz
                self.text_resultados.delete("1.0", tk.END)
                self.text_resultados.insert(tk.END, "Matriz reducida (RREF):\n")
                for fila in matriz:
                    self.text_resultados.insert(tk.END, " | ".join(f"{x:8.3f}" for x in fila) + "\n")
                self.text_resultados.insert(tk.END, "\nSoluciones:\n")
                for i, val in enumerate(soluciones, start=1):
                    self.text_resultados.insert(tk.END, f"x{i} = {val:.3f}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar(self):
        self.generar_campos()
        self.text_resultados.delete("1.0", tk.END)
        self.logica.limpiar()

if __name__ == "__main__":
    app = App()
    app.mainloop()
