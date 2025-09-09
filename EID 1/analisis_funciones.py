import sympy as sp
from sympy.calculus.util import continuous_domain, function_range, Reals

def calcular_dominio(funcion_str):
    """
    Calcula el dominio de una funcion dada
    """
    x = sp.Symbol('x')
    try:
        funcion = sp.sympify(funcion_str)
        # Usa la funcion continuous_domain de sympy para encontrar el dominio
        dominio_simbolico = continuous_domain(funcion, x, Reals)
        dominio_str = str(dominio_simbolico).replace('Reals', 'Todos los numeros reales')
        return dominio_str
    except Exception as e:
        return f"Error al calcular el dominio: {e}"

def calcular_recorrido(funcion_str):
    """
    Calcula el recorrido (rango) de una funcion dada
    """
    x = sp.Symbol('x')
    try:
        funcion = sp.sympify(funcion_str)
        # Usa la funcion function_range de sympy para encontrar el recorrido
        recorrido_simbolico = function_range(funcion, x, Reals)
        recorrido_str = str(recorrido_simbolico).replace('Reals', 'Todos los numeros reales')
        return recorrido_str
    except Exception as e:
        return f"Error al calcular el recorrido: {e}"

def calcular_intersecciones(funcion_str):
    """
    Calcula las intersecciones con los ejes x e y
    """
    x = sp.Symbol('x')
    try:
        funcion = sp.sympify(funcion_str)
        # Para el eje y, se reemplaza x = 0 y se calcula el valor
        y_int = funcion.subs(x, 0)
        y_int_str = f"(0, {y_int})"

        # Para el eje x, se resuelve la ecuacion f(x) = 0
        x_intersecciones = sp.solve(funcion, x)
        x_int_str = f"({', '.join(map(str, x_intersecciones))}, 0)"

        return y_int_str, x_int_str
    except Exception as e:
        return f"Error al calcular intersecciones: {e}", ""

def evaluar_punto(funcion_str, valor_x_str):
    """
    Evalua un punto en la funcion y muestra el paso a paso
    """
    x = sp.Symbol('x')
    try:
        # Convierte la cadena en una expresion de sympy
        funcion = sp.sympify(funcion_str)
        valor_x = sp.sympify(valor_x_str)
        
        # Muestra el paso a paso del resultado
        paso_a_paso = f"Evaluando f({valor_x}) = {funcion.subs(x, valor_x)}\n"
        paso_a_paso += "------------------------\n"
        paso_a_paso += f"Sustituyendo el valor en la función: {funcion_str}\n"
        paso_a_paso += f"Paso 1: f({valor_x}) = {funcion.subs(x, valor_x)}\n"
        
        # Evalua el numero
        punto_y = funcion.subs(x, valor_x).evalf()
        
        return paso_a_paso, (valor_x, punto_y)
    except Exception as e:
        return f"Ocurrió un error al evaluar el punto: {e}", None
