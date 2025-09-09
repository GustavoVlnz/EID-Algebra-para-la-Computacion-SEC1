import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def generar_grafico(funcion_str, punto_evaluado=None):
    """
    genera y muestra el grafico de la funcion, incluyendo el punto evaluado
    """
    x = sp.Symbol('x')
    try:
        funcion = sp.sympify(funcion_str)
        # genera los puntos para el grafico
        x_vals = np.linspace(-10, 10, 400)
        y_vals = [funcion.subs(x, val) for val in x_vals]
        
        # crea el grafico
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, label=f'f(x) = {funcion_str}')
        
        # resalta el punto evaluado en caso de existir
        if punto_evaluado:
            plt.scatter(punto_evaluado[0], punto_evaluado[1], color='red', s=100, zorder=5, label=f'Punto Evaluado: ({punto_evaluado[0]}, {punto_evaluado[1]})')
        
        # configuraciones para el estilo del grafico y mostrarlo en pantalla
        plt.title('Gráfico de la Función')
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.grid(True)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"Error al generar el gráfico: {e}")
