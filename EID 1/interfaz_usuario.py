import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# simulando importaciones de los otros archivos
# en tu proyecto final estas lineas deben ser las reales
def calcular_dominio(func):
    return "Simulando calculo de dominio..."

def calcular_intersecciones(func):
    return ("(0, y_int)", "(x_int, 0)")

def evaluar_punto(func, val):
    return f"Simulando paso a paso para x={val}", (val, 1)

def generar_grafico(func, punto=None):
    messagebox.showinfo("Grafico", "Se generaria un grafico aqui...")

class FunctionAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Funciones")
        self.root.geometry("1000x650")
        
        # estilo para que se vea mas claro y minimalista
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#F0F0F0')  # fondo claro
        self.style.configure('TLabelFrame', background='#FFFFFF', foreground='#333333', font=('Arial', 12, 'bold')) # contenedor blanco con texto oscuro
        self.style.configure('TLabel', background='#FFFFFF', foreground='#333333', font=('Arial', 11))
        self.style.configure('TEntry', font=('Arial', 11), fieldbackground='#FFFFFF', foreground='#333333') # campos de entrada claros
        
        # colores para los botones
        self.style.configure('TButton', font=('Arial', 11, 'bold'), padding=8, background='#007BFF', foreground='white') # azul brillante
        self.style.map('TButton', background=[('active', '#0056b3'), ('!disabled', '#007BFF')])

        self.setup_ui()

    def setup_ui(self):
        # frame principal para el diseno de la interfaz
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # el titulo del programa
        title_label = ttk.Label(main_frame, text="Analizador de Funciones", font=("Arial", 24, "bold"), background='#F0F0F0', foreground='#007BFF') # azul para el titulo
        title_label.pack(pady=10)

        # seccion de entrada de la funcion
        input_frame = ttk.LabelFrame(main_frame, text="Entrada de la Funcion", padding="15")
        input_frame.pack(fill=tk.X, pady=15)

        func_label = ttk.Label(input_frame, text="Funcion f(x):")
        func_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.function_entry = ttk.Entry(input_frame, width=40)
        self.function_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        eval_label = ttk.Label(input_frame, text="Valor para evaluar x:")
        eval_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.eval_entry = ttk.Entry(input_frame, width=15)
        self.eval_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        # botones para analizar, limpiar y ayuda
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(pady=15)

        analyze_button = ttk.Button(button_frame, text="Analizar y Graficar", command=self.analyze_and_plot)
        analyze_button.pack(side=tk.LEFT, padx=15)
        
        clear_button = ttk.Button(button_frame, text="Limpiar", command=self.clear_fields)
        clear_button.pack(side=tk.LEFT, padx=15)
        
        help_button = ttk.Button(button_frame, text="Ayuda", command=self.show_help)
        help_button.pack(side=tk.LEFT, padx=15)

        # seccion para los resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="15")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=15)

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, state='disabled', font=('Arial', 10), padx=5, pady=5, background='#FFFFFF', foreground='#333333', insertbackground='black')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
    def analyze_and_plot(self):
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        function_str = self.function_entry.get()
        eval_str = self.eval_entry.get()

        if not function_str:
            self.results_text.insert(tk.END, "Error: Por favor, ingrese una funcion\n")
            self.results_text.config(state='disabled')
            return

        try:
            dominio = calcular_dominio(function_str)
            y_int, x_int = calcular_intersecciones(function_str)
            
            output = " Analisis Matematico \n"
            output += f"Dominio: {dominio}\n"
            output += f"Interseccion con el Eje Y: {y_int}\n"
            output += f"Interseccion con el Eje X: {x_int}\n"
            
            punto_evaluado = None
            if eval_str:
                paso_a_paso, punto = evaluar_punto(function_str, eval_str)
                output += "\n Evaluacion del Punto \n"
                output += paso_a_paso
                punto_evaluado = punto
            
            self.results_text.insert(tk.END, output)

            generar_grafico(function_str, punto_evaluado)

        except Exception as e:
            self.results_text.insert(tk.END, f"Ocurrio un error: {e}")
        
        self.results_text.config(state='disabled')

    def clear_fields(self):
        self.function_entry.delete(0, tk.END)
        self.eval_entry.delete(0, tk.END)
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')

    def show_help(self):
        help_message = """
        **Como ingresar una funcion:**
        
        Utilice los siguientes operadores para escribir su funcion en el campo "Funcion f(x)":
        
        +   Suma: Para sumar terminos Ejemplo: x + 2
        -   Resta: Para restar terminos Ejemplo: x - 5
        * Multiplicacion: Use un asterisco para multiplicar Ejemplo: 3*x
        /   Division: Para crear funciones racionales Ejemplo: (x + 1) / (x - 2)
        ** Exponente: Use dos asteriscos para potencias Ejemplo: x**2 para x²
        
        **Ejemplos:**
        
        - Para 3x**2 + 2x - 1, ingrese: 3*x**2 + 2*x - 1
        - Para (x+1)/(x-2), ingrese: (x+1)/(x-2)
        """
        messagebox.showinfo("Ayuda - Sintaxis de la Funcion", help_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionAnalyzerApp(root)
    root.mainloop()
