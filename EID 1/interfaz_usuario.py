import tkinter as tk
from tkinter import messagebox
from analisis_funciones import AnalizadorFunciones
from visualizacion_graficos import graficar_funcion

class AnalizadorFuncionesGUI(tk.Tk):
    def __init__(self, backend):
        super().__init__()
        
        self.backend = backend
        self.title("Analizador de Funciones")
        self.geometry("800x600")
        self.config(bg="#E6E6E6") 

        self.resizable(False, False)

        self.setup_ui()

        # --- Centrar la ventana ---
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        self.config(bg="#E6E6E6")
        
    def setup_ui(self):
        # Frame principal para centrar el contenido y aplicar margenes
        main_frame = tk.Frame(self, bg="#E6E6E6", padx=50, pady=50)
        main_frame.pack(expand=True, fill="both")
        
        # Etiqueta e input para la funcion
        label_funcion = tk.Label(main_frame, text="Ingresa la funcion f(x):", bg="#E6E6E6", font=("Arial", 14, "bold"), fg="#333333")
        label_funcion.pack(pady=(0, 5))
        
        self.input_funcion = tk.Entry(main_frame, width=40, font=("Arial", 12))
        self.input_funcion.pack()
        self.input_funcion.insert(0, "ej: 2*x**2 + 3*x - 5") 
        
        # Estilo para el texto placeholder
        self.input_funcion.config(foreground="#A0A0A0")

        # Espacio entre inputs
        spacer1 = tk.Frame(main_frame, height=30, bg="#E6E6E6") 
        spacer1.pack()
        
        # Etiqueta e input para el valor a evaluar
        label_evaluar = tk.Label(main_frame, text="Ingresa un valor para evaluar (opcional):", bg="#E6E6E6", font=("Arial", 14, "bold"), fg="#333333")
        label_evaluar.pack(pady=(0, 5))
        
        self.input_evaluar = tk.Entry(main_frame, width=40, font=("Arial", 12))
        self.input_evaluar.pack()
        self.input_evaluar.insert(0, "ej: 2 o 0.5")
        
        # Estilo para el texto placeholder
        self.input_evaluar.config(foreground="#A0A0A0")
        
        # Frame para los botones
        button_frame = tk.Frame(main_frame, bg="#E6E6E6")
        button_frame.pack(pady=20)
        
        # Colores de los botones
        self.color_analizar = '#4CAF50'
        self.color_analizar_hover = '#367c39'
        self.color_limpiar = '#F44336'
        self.color_limpiar_hover = '#c82333'
        self.color_ayuda = '#2196F3'
        self.color_ayuda_hover = '#1976D2'

        # Botones de accion
        self.boton_limpiar = tk.Button(button_frame, text="Limpiar", command=self.limpiar_campos, 
                                     bg=self.color_limpiar, fg='white', font=("Arial", 12, "bold"), 
                                     relief='flat', padx=15, pady=8, bd=0)
        self.boton_limpiar.pack(side="left", padx=5)
        self.boton_limpiar.bind("<Enter>", lambda e: self.on_enter(e, self.color_limpiar_hover))
        self.boton_limpiar.bind("<Leave>", lambda e: self.on_leave(e, self.color_limpiar))

        self.boton_analizar = tk.Button(button_frame, text="Analizar y Graficar", command=self.analizar_y_graficar, 
                                      bg=self.color_analizar, fg='white', font=("Arial", 12, "bold"), 
                                      relief='flat', padx=15, pady=8, bd=0)
        self.boton_analizar.pack(side="left", padx=5)
        self.boton_analizar.bind("<Enter>", lambda e: self.on_enter(e, self.color_analizar_hover))
        self.boton_analizar.bind("<Leave>", lambda e: self.on_leave(e, self.color_analizar))

        self.boton_ayuda = tk.Button(button_frame, text="Ayuda", command=self.mostrar_ayuda, 
                                    bg=self.color_ayuda, fg='white', font=("Arial", 12, "bold"), 
                                    relief='flat', padx=15, pady=8, bd=0)
        self.boton_ayuda.pack(side="left", padx=5)
        self.boton_ayuda.bind("<Enter>", lambda e: self.on_enter(e, self.color_ayuda_hover))
        self.boton_ayuda.bind("<Leave>", lambda e: self.on_leave(e, self.color_ayuda))

        # Area de resultados
        self.output_area = tk.Text(main_frame, height=10, width=60, font=("Arial", 12), bg='#F8F8F8', bd=1, relief="flat")
        self.output_area.pack(pady=(10, 0), expand=True, fill="both")
        
        # Vincular eventos para el texto placeholder
        self.input_funcion.bind("<FocusIn>", lambda event: self.on_focus_in(self.input_funcion, "ej: 2*x**2 + 3*x - 5"))
        self.input_funcion.bind("<FocusOut>", lambda event: self.on_focus_out(self.input_funcion, "ej: 2*x**2 + 3*x - 5"))
        self.input_evaluar.bind("<FocusIn>", lambda event: self.on_focus_in(self.input_evaluar, "ej: 2 o 0.5"))
        self.input_evaluar.bind("<FocusOut>", lambda event: self.on_focus_out(self.input_evaluar, "ej: 2 o 0.5"))

    def on_enter(self, event, color):
        event.widget.config(bg=color)

    def on_leave(self, event, color):
        event.widget.config(bg=color)

    def on_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='#333333')

    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(foreground='#A0A0A0')
            
    def analizar_y_graficar(self):
        funcion_str = self.input_funcion.get()
        valor_evaluar_str = self.input_evaluar.get()
        
        if funcion_str == "ej: 2*x**2 + 3*x - 5":
            funcion_str = ""
        if valor_evaluar_str == "ej: 2 o 0.5":
            valor_evaluar_str = ""
            
        if not funcion_str:
            messagebox.showwarning("Error de entrada", "No ingresaste ninguna funcion")
            return

        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, "Analizando...\n")
        
        # Realizando el analisis matematico
        dominio = self.backend.calcular_dominio(funcion_str)
        recorrido = self.backend.calcular_recorrido(funcion_str)
        interseccion_y, interseccion_x = self.backend.calcular_intersecciones(funcion_str)
        
        resultados_str = f"Dominio: {dominio}\n"
        resultados_str += f"Recorrido: {recorrido}\n"
        resultados_str += f"{interseccion_y}\n"
        resultados_str += f"{interseccion_x}\n"
        
        punto_evaluado = None
        if valor_evaluar_str:
            try:
                valor_evaluar = float(valor_evaluar_str)
                resultado_eval, pasos = self.backend.evaluar_funcion(funcion_str, valor_evaluar)
                if isinstance(resultado_eval, str):
                    messagebox.showerror("Error al evaluar", resultado_eval)
                    return
                resultados_str += "\n--- Evaluacion ---\n"
                resultados_str += "\n".join(pasos)
                resultados_str += f"\nPar ordenado: ({valor_evaluar}, {resultado_eval})"
                punto_evaluado = (valor_evaluar, resultado_eval)
            except ValueError:
                messagebox.showerror("Error de entrada", "El valor para evaluar no es un numero")
                return
        
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, resultados_str)
        
        # Llamando al modulo de graficado
        graficar_funcion(funcion_str, punto_evaluado=punto_evaluado, intersecciones=(interseccion_x, interseccion_y))

    def limpiar_campos(self):
        # Funcion mejorada para limpiar los campos solo si hay contenido
        output_content = self.output_area.get("1.0", tk.END).strip()
        funcion_content = self.input_funcion.get().strip()
        evaluar_content = self.input_evaluar.get().strip()
        
        # Verificamos si hay contenido real para limpiar
        if not output_content and funcion_content == "ej: 2*x**2 + 3*x - 5" and evaluar_content == "ej: 2 o 0.5":
            messagebox.showinfo("Limpiar", "No hay nada que limpiar")
            return

        # Si hay contenido, procedemos a limpiar
        self.input_funcion.delete(0, tk.END)
        self.input_funcion.insert(0, "ej: 2*x**2 + 3*x - 5")
        self.input_funcion.config(foreground='#A0A0A0')
        
        self.input_evaluar.delete(0, tk.END)
        self.input_evaluar.insert(0, "ej: 2 o 0.5")
        self.input_evaluar.config(foreground='#A0A0A0')
        
        self.output_area.delete("1.0", tk.END)
        messagebox.showinfo("Limpiar", "Campos limpiados correctamente")

    def mostrar_ayuda(self):
        mensaje = """
            Para ingresar funciones, utiliza la siguiente sintaxis:
            
            - Suma: +
            - Resta: -
            - Multiplicacion: *
            - Division: /
            - Potencia: ** o ^
            - Raiz cuadrada: sqrt(x)
            
            Ejemplos de funciones:
            - Funcion lineal: 2*x + 3
            - Funcion cuadratica: x**2 - 4*x
            - Funcion racional: (x - 1) / (x + 2)
            - Funcion con raiz: sqrt(x + 1)
        """
        messagebox.showinfo("Ayuda de Sintaxis", mensaje)






# interfaz_usuario.py

import tkinter as tk
from tkinter import messagebox
from analisis_funciones import AnalizadorFunciones
from visualizacion_graficos import graficar_funcion

class AnalizadorFuncionesGUI(tk.Tk):
    def __init__(self, backend):
        super().__init__()
        
        self.backend = backend
        self.title("Analizador de Funciones")
        
        # --- LINEA MODIFICADA: Ventana no redimensionable ---
        self.resizable(False, False)
        
        # --- LINEAS AÑADIDAS: Centrar la ventana ---
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        self.config(bg="#E6E6E6") 

        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal para centrar el contenido y aplicar margenes
        main_frame = tk.Frame(self, bg="#E6E6E6", padx=50, pady=50)
        main_frame.pack(expand=True, fill="both")
        
        # Etiqueta e input para la funcion
        label_funcion = tk.Label(main_frame, text="Ingresa la funcion f(x):", bg="#E6E6E6", font=("Arial", 14, "bold"), fg="#333333")
        label_funcion.pack(pady=(0, 5))
        
        self.input_funcion = tk.Entry(main_frame, width=40, font=("Arial", 12))
        self.input_funcion.pack()
        self.input_funcion.insert(0, "ej: 2*x**2 + 3*x - 5") 
        
        # Estilo para el texto placeholder
        self.input_funcion.config(foreground="#A0A0A0")

        # Espacio entre inputs
        spacer1 = tk.Frame(main_frame, height=30, bg="#E6E6E6") 
        spacer1.pack()
        
        # Etiqueta e input para el valor a evaluar
        label_evaluar = tk.Label(main_frame, text="Ingresa un valor para evaluar (opcional):", bg="#E6E6E6", font=("Arial", 14, "bold"), fg="#333333")
        label_evaluar.pack(pady=(0, 5))
        
        self.input_evaluar = tk.Entry(main_frame, width=40, font=("Arial", 12))
        self.input_evaluar.pack()
        self.input_evaluar.insert(0, "ej: 2 o 0.5")
        
        # Estilo para el texto placeholder
        self.input_evaluar.config(foreground="#A0A0A0")
        
        # Frame para los botones
        button_frame = tk.Frame(main_frame, bg="#E6E6E6")
        button_frame.pack(pady=20)
        
        # Colores de los botones
        self.color_analizar = '#4CAF50'
        self.color_analizar_hover = '#367c39'
        self.color_limpiar = '#F44336'
        self.color_limpiar_hover = '#c82333'
        self.color_ayuda = '#2196F3'
        self.color_ayuda_hover = '#1976D2'

        # Botones de accion
        self.boton_limpiar = tk.Button(button_frame, text="Limpiar", command=self.limpiar_campos, 
                                     bg=self.color_limpiar, fg='white', font=("Arial", 12, "bold"), 
                                     relief='flat', padx=15, pady=8, bd=0)
        self.boton_limpiar.pack(side="left", padx=5)
        self.boton_limpiar.bind("<Enter>", lambda e: self.on_enter(e, self.color_limpiar_hover))
        self.boton_limpiar.bind("<Leave>", lambda e: self.on_leave(e, self.color_limpiar))

        self.boton_analizar = tk.Button(button_frame, text="Analizar y Graficar", command=self.analizar_y_graficar, 
                                      bg=self.color_analizar, fg='white', font=("Arial", 12, "bold"), 
                                      relief='flat', padx=15, pady=8, bd=0)
        self.boton_analizar.pack(side="left", padx=5)
        self.boton_analizar.bind("<Enter>", lambda e: self.on_enter(e, self.color_analizar_hover))
        self.boton_analizar.bind("<Leave>", lambda e: self.on_leave(e, self.color_analizar))

        self.boton_ayuda = tk.Button(button_frame, text="Ayuda", command=self.mostrar_ayuda, 
                                    bg=self.color_ayuda, fg='white', font=("Arial", 12, "bold"), 
                                    relief='flat', padx=15, pady=8, bd=0)
        self.boton_ayuda.pack(side="left", padx=5)
        self.boton_ayuda.bind("<Enter>", lambda e: self.on_enter(e, self.color_ayuda_hover))
        self.boton_ayuda.bind("<Leave>", lambda e: self.on_leave(e, self.color_ayuda))

        # Area de resultados
        self.output_area = tk.Text(main_frame, height=10, width=60, font=("Arial", 12), bg='#F8F8F8', bd=1, relief="flat")
        self.output_area.pack(pady=(10, 0), expand=True, fill="both")
        
        # Vincular eventos para el texto placeholder
        self.input_funcion.bind("<FocusIn>", lambda event: self.on_focus_in(self.input_funcion, "ej: 2*x**2 + 3*x - 5"))
        self.input_funcion.bind("<FocusOut>", lambda event: self.on_focus_out(self.input_funcion, "ej: 2*x**2 + 3*x - 5"))
        self.input_evaluar.bind("<FocusIn>", lambda event: self.on_focus_in(self.input_evaluar, "ej: 2 o 0.5"))
        self.input_evaluar.bind("<FocusOut>", lambda event: self.on_focus_out(self.input_evaluar, "ej: 2 o 0.5"))

    def on_enter(self, event, color):
        event.widget.config(bg=color)

    def on_leave(self, event, color):
        event.widget.config(bg=color)

    def on_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='#333333')

    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(foreground='#A0A0A0')
            
    def analizar_y_graficar(self):
        funcion_str = self.input_funcion.get()
        valor_evaluar_str = self.input_evaluar.get()
        
        if funcion_str == "ej: 2*x**2 + 3*x - 5":
            funcion_str = ""
        if valor_evaluar_str == "ej: 2 o 0.5":
            valor_evaluar_str = ""
            
        if not funcion_str:
            messagebox.showwarning("Error de entrada", "No me pasaste ninguna funcion eh, intentalo de nuevo")
            return

        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, "Analizando...\n")
        
        # Realizando el analisis matematico
        dominio = self.backend.calcular_dominio(funcion_str)
        recorrido = self.backend.calcular_recorrido(funcion_str)
        interseccion_y, interseccion_x = self.backend.calcular_intersecciones(funcion_str)
        
        resultados_str = f"Dominio: {dominio}\n"
        resultados_str += f"Recorrido: {recorrido}\n"
        resultados_str += f"{interseccion_y}\n"
        resultados_str += f"{interseccion_x}\n"
        
        punto_evaluado = None
        if valor_evaluar_str:
            try:
                valor_evaluar = float(valor_evaluar_str)
                resultado_eval, pasos = self.backend.evaluar_funcion(funcion_str, valor_evaluar)
                if isinstance(resultado_eval, str):
                    messagebox.showerror("Error al evaluar", resultado_eval)
                    return
                resultados_str += "\n--- Evaluacion ---\n"
                resultados_str += "\n".join(pasos)
                resultados_str += f"\nPar ordenado: ({valor_evaluar}, {resultado_eval})"
                punto_evaluado = (valor_evaluar, resultado_eval)
            except ValueError:
                messagebox.showerror("Error de entrada", "El valor para evaluar no es un numero")
                return
        
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, resultados_str)
        
        # Llamando al modulo de graficado
        graficar_funcion(funcion_str, punto_evaluado=punto_evaluado, intersecciones=(interseccion_x, interseccion_y))

    def limpiar_campos(self):
        # Funcion mejorada para limpiar los campos solo si hay contenido
        output_content = self.output_area.get("1.0", tk.END).strip()
        funcion_content = self.input_funcion.get().strip()
        evaluar_content = self.input_evaluar.get().strip()
        
        # Verificamos si hay contenido real para limpiar
        if not output_content and funcion_content == "ej: 2*x**2 + 3*x - 5" and evaluar_content == "ej: 2 o 0.5":
            messagebox.showinfo("Limpiar", "No hay nada que limpiar.")
            return

        # Si hay contenido, procedemos a limpiar
        self.input_funcion.delete(0, tk.END)
        self.input_funcion.insert(0, "ej: 2*x**2 + 3*x - 5")
        self.input_funcion.config(foreground='#A0A0A0')
        
        self.input_evaluar.delete(0, tk.END)
        self.input_evaluar.insert(0, "ej: 2 o 0.5")
        self.input_evaluar.config(foreground='#A0A0A0')
        
        self.output_area.delete("1.0", tk.END)
        messagebox.showinfo("Limpiar", "Campos limpiados correctamente!")

    def mostrar_ayuda(self):
        mensaje = """
            Para ingresar funciones, utiliza la siguiente sintaxis:
            
            - Suma: +
            - Resta: -
            - Multiplicacion: *
            - Division: /
            - Potencia: ** o ^
            - Raiz cuadrada: sqrt(x)
            
            Ejemplos de funciones:
            - Funcion lineal: 2*x + 3
            - Funcion cuadratica: x**2 - 4*x
            - Funcion racional: (x - 1) / (x + 2)
            - Funcion con raiz: sqrt(x + 1)
        """
        messagebox.showinfo("Ayuda de Sintaxis", mensaje)
