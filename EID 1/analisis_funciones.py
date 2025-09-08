import sympy as sp

def calcular_dominio(funcion):
    """
    Calcula el dominio de una función dada.
    """
    x = sp.Symbol('x')
    try:
        # encuentra las restricciones del dominio
        restricciones = sp.solve(sp.denom(funcion), x)
        if restricciones:
            dominio_str = f"Todos los numeros reales excepto los valores donde el denominador es cero: x ≠ {', '.join(map(str, restricciones))}"
        else:
            dominio_str = "Todos los numeros reales."
        return dominio_str
    except Exception as e:
        return f"Error al calcular el dominio: {e}"

def calcular_intersecciones(funcion):
    """
    Calcula las intersecciones con los ejes x e y.
    """
    x = sp.Symbol('x')
    try:
        # para el eje y, se reemplaza x = 0 y se calcula el valor en ese punto
        y_int = funcion.subs(x, 0)
        y_int_str = f"(0, {y_int})"

        # para el eje x, se resuelve la ecuación f(x) = 0
        x_intersecciones = sp.solve(funcion, x)
        x_int_str = f"({', '.join(map(str, x_intersecciones))}, 0)"

        return y_int_str, x_int_str
    except Exception as e:
        return f"Error al calcular intersecciones: {e}", ""

def evaluar_punto(funcion_str, valor_x_str):
    """
    Evalua un punto en la funcion y muestra el paso a paso.
    """
    x = sp.Symbol('x')
    try:
        #convierte la cadena en una expresión de sympy
        funcion = sp.sympify(funcion_str)
        valor_x = sp.sympify(valor_x_str)
        
        #mostrar el paso a paso del resultado
        paso_a_paso = f"Función: f(x) = {funcion}\n"
        paso_a_paso += f"Evaluando en x = {valor_x}:\n"
        paso_a_paso += f"f({valor_x}) = {funcion.subs(x, valor_x)}\n"
        
        #calcula el resutlado de la funcion
        resultado = funcion.subs(x, valor_x)
        
        return paso_a_paso, (valor_x, resultado)
    except Exception as e:
        return f"Error al evaluar el punto: {e}", None