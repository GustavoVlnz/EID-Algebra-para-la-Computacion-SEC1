import sympy as sp

class AnalizadorFunciones:
    def __init__(self):
        pass

    def evaluar_funcion(self, funcion_str, x_val):
        # Manejo de errores para la expresion
        try:
            x = sp.Symbol('x')
            f_x = sp.sympify(funcion_str)
            
            # Chequeando que el valor sea valido para la funcion
            if f_x.subs(x, x_val).is_complex:
                return "Error: el valor de x genera un numero complejo", None
            
            resultado = f_x.subs(x, x_val)
            pasos = self.obtener_pasos_evaluacion(funcion_str, x_val, resultado)
            
            return resultado, pasos
        except sp.SympifyError:
            return "Error: funcion no valida", None
        except ZeroDivisionError:
            return "Error: division por cero en ese punto", None
        except Exception as e:
            return f"Error inesperado: {e}", None

    def obtener_pasos_evaluacion(self, funcion_str, x_val, resultado):
        # Esto es un ejemplo, se puede mejorar
        pasos = [
            f"Funcion original: f(x) = {funcion_str}",
            f"Sustituyendo x por {x_val}: f({x_val}) = {funcion_str.replace('x', str(x_val))}",
            f"Calculando: f({x_val}) = {resultado}"
        ]
        return pasos
    
    def calcular_dominio(self, funcion_str):
        # Placeholder para el calculo del dominio
        # La logica real seria mas compleja para funciones racionales o con raices
        x = sp.Symbol('x')
        f_x = sp.sympify(funcion_str)

        dominio = "Todos los numeros reales" # Caso por defecto
        
        # Ejemplo para funcion racional
        if '/' in funcion_str:
            numerador, denominador = funcion_str.split('/')
            denominador_expr = sp.sympify(denominador)
            restricciones = sp.solve(denominador_expr, x)
            if restricciones:
                dominio = f"Dominio: x pertenece a R, excepto cuando x es {restricciones}"
        
        return dominio

    def calcular_recorrido(self, funcion_str):
        # Este calculo es mas complejo y a menudo requiere analisis mas profundo
        # Aqui solo un placeholder simple
        recorrido = "No implementado aun, es mas complejo"
        return recorrido

    def calcular_intersecciones(self, funcion_str):
        # Placeholder para las intersecciones
        x = sp.Symbol('x')
        f_x = sp.sympify(funcion_str)
        
        # Interseccion con el eje y (x=0)
        y_int = f_x.subs(x, 0)
        
        # Interseccion con el eje x (f(x)=0)
        x_int = sp.solve(f_x, x)
        
        return f"Interseccion Y: ({0}, {y_int})", f"Intersecciones X: {x_int}"
