import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Declaramos la figura y el eje de forma global para poder reutilizarlos
fig, ax = None, None

def graficar_funcion(funcion_str, punto_evaluado=None, intersecciones=None):
    global fig, ax

    # Si la figura ya existe, la limpiamos para no superponer graficos
    if fig and ax:
        ax.clear()
    else:
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(8, 6))

    try:
        x = sp.Symbol('x')
        f_x = sp.sympify(funcion_str)

        # Creando un rango de valores para graficar
        x_vals = np.linspace(-10, 10, 400)
        y_vals = sp.lambdify(x, f_x, 'numpy')(x_vals)

        # Manejando asintotas de forma simple
        y_vals[np.abs(y_vals) > 50] = np.nan
        
        # Graficando la funcion
        ax.plot(x_vals, y_vals, color='#1f77b4', label=f'f(x) = {funcion_str}')
        
        # Resaltando las intersecciones
        if intersecciones:
            x_int_str, y_int_str = intersecciones
            if "x_int" in x_int_str:
                x_intersecciones = eval(x_int_str.split(': ')[1])
                for x_int in x_intersecciones:
                    ax.plot(x_int, 0, 'o', color='#2ca02c', label='Interseccion X' if x_int == x_intersecciones[0] else "")
            
            y_interseccion = eval(y_int_str.split(': ')[1])
            ax.plot(y_interseccion[0], y_interseccion[1], 'o', color='#d62728', label='Interseccion Y')

        # Resaltando el punto evaluado si existe
        if punto_evaluado:
            ax.plot(punto_evaluado[0], punto_evaluado[1], 'o', color='#ff7f0e', markersize=8, label=f'Punto Evaluado: ({punto_evaluado[0]}, {punto_evaluado[1]})')

        # Configurando el grafico para que se vea profesional
        ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
        ax.axvline(0, color='gray', linewidth=0.5, linestyle='--')
        ax.set_title(f'Grafico de la funcion {funcion_str}', fontsize=16)
        ax.set_xlabel('Eje X', fontsize=12)
        ax.set_ylabel('Eje Y', fontsize=12)
        ax.legend()
        plt.show()

    except Exception as e:
        print(f"Error al graficar: {e}")
