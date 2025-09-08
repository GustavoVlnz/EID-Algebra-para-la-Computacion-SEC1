import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from analisis_funciones import calcular_dominio, calcular_intersecciones, evaluar_punto
from visualizacion_graficos import generar_grafico

class FunctionAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Funciones")
        self.root.geometry("1000x600")

        self.setup_ui()

    def setup_ui(self):
        # frame principal para el diseño de la interfaz
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # seccion de entrada para la funcion
        input_frame = ttk.LabelFrame(main_frame, text="Entrada de la Funcion", padding="10")
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="Funcion f(x):").pack(side=tk.LEFT, padx=5)
        self.function_entry = ttk.Entry(input_frame, width=40)
        self.function_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Label(input_frame, text="Valor para evaluar x:").pack(side=tk.LEFT, padx=5)
        self.eval_entry = ttk.Entry(input_frame, width=15)
        self.eval_entry.pack(side=tk.LEFT, padx=5)
        
        # botones para analizar, limpiar y ayuda
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        analyze_button = ttk.Button(button_frame, text="Analizar y Graficar", command=self.analyze_and_plot)
        analyze_button.pack(side=tk.LEFT, padx=10)
        
        clear_button = ttk.Button(button_frame, text="Limpiar", command=self.clear_fields)
        clear_button.pack(side=tk.LEFT, padx=10)
        
        help_button = ttk.Button(button_frame, text="Ayuda", command=self.show_help)
        help_button.pack(side=tk.LEFT, padx=10)

        # seccion de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, state='disabled')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
    def analyze_and_plot(self):
        # habilita el area de texto para escribir
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        function_str = self.function_entry.get()
        eval_str = self.eval_entry.get()

        if not function_str:
            self.results_text.insert(tk.END, "Error: Por favor, ingrese una funcion.\n")
            self.results_text.config(state='disabled')
            return

        try:
            # llama a las funciones del modulo analisis_funciones
            dominio = calcular_dominio(function_str)
            y_int, x_int = calcular_intersecciones(function_str)
            
            output = "--- Analisis Matematico ---\n"
            output += f"Dominio: {dominio}\n"
            output += f"Interseccion con el Eje Y: {y_int}\n"
            output += f"Interseccion con el Eje X: {x_int}\n"
            # evaluar el punto si se ingreso un valor
            punto_evaluado = None
            if eval_str:
                paso_a_paso, punto = evaluar_punto(function_str, eval_str)
                output += "\n--- Evaluacion del Punto ---\n"
                output += paso_a_paso
                punto_evaluado = punto
            
            self.results_text.insert(tk.END, output)

            # llama a la funcion de visualizacion para generar el grafico
            generar_grafico(function_str, punto_evaluado)

        except Exception as e:
            self.results_text.insert(tk.END, f"Ocurrio un error: {e}")
        
        self.results_text.config(state='disabled')

    #funcion para limpiar los campos de entrada
    def clear_fields(self):
        self.function_entry.delete(0, tk.END)
        self.eval_entry.delete(0, tk.END)
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')

    #funcion para mostrar la ayuda
    def show_help(self):
        help_message = """
        **Como ingresar una funcion:**
        
        Utilice los siguientes operadores para escribir su funcion en el campo "Funcion f(x)":
        
        +   Suma: Para sumar terminos. Ejemplo: x + 2
        -   Resta: Para restar terminos. Ejemplo: x - 5
        * Multiplicacion: Use un asterisco para multiplicar. Ejemplo: 3*x
        /   Division: Para crear funciones racionales. Ejemplo: (x + 1) / (x - 2)
        ** Exponente: Use dos asteriscos para potencias. Ejemplo: x**2 para x²
        
        **Ejemplos:**
        
        - Para 3x² + 2x - 1, ingrese: 3*x**2 + 2*x - 1
        - Para (x+1)/(x-2), ingrese: (x+1)/(x-2)
        """
        messagebox.showinfo("Ayuda - Sintaxis de la Funcion", help_message)

#ejecucion del programa
if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionAnalyzerApp(root)
    root.mainloop()