import sympy as sp

class AnalizadorFunciones:
    def __init__(self):
        pass

    # validacion de entrada
    def validar_funcion(self, funcion_str):
        """
        valida que la funcion sea polinomica o racional
        devuelve True/False y un mensaje explicativo
        """
        try:
            if not funcion_str or funcion_str.strip() == "":
                return False, "La funcion no puede estar vacia"
            
            x = sp.Symbol('x')
            f_x = sp.sympify(funcion_str)
            
            # verifica que contenga la variable x
            if not f_x.has(x):
                return False, "La funcion debe contener la variable x"
            
            # verifica que solo sean funciones polinomicas o racionales
            funciones_no_permitidas = [sp.sin, sp.cos, sp.tan, sp.log, sp.exp, sp.sqrt]
            atoms = f_x.atoms(sp.Function)
            
            for atom in atoms:
                if any(isinstance(atom, func) for func in funciones_no_permitidas):
                    return False, "Solo se permiten funciones polinomicas y racionales"
            
            return True, "Funcion valida"
            
        except sp.SympifyError:
            return False, "Formato de funcion invalido"
        except Exception as e:
            return False, f"Error al validar la funcion: {e}"

    # evaluacion de la funcion
    def evaluar_funcion(self, funcion_str, x_val):
        """
        evalua una funcion en un valor de x con pasos detallados
        incluye validacion de funcion y dominio
        """
        # validar la funcion primero
        es_valida, mensaje = self.validar_funcion(funcion_str)
        if not es_valida:
            return f"Error: {mensaje}", None

        try:
            # validar que x_val sea un numero
            try:
                x_val = float(x_val)
            except (ValueError, TypeError):
                return "Error: el valor de x debe ser un numero", None
            
            x = sp.Symbol('x')
            f_x = sp.sympify(funcion_str)
            
            # revisar si el valor esta en el dominio
            if not self.esta_en_dominio(f_x, x_val):
                return "Error: el valor esta fuera del dominio de la funcion", None
            
            resultado = f_x.subs(x, x_val)

            # revisar si el resultado es valido
            if resultado.is_complex or resultado.has(sp.I):
                return "Error: el valor de x genera un numero complejo", None
            if resultado.has(sp.oo) or resultado.has(-sp.oo) or resultado.has(sp.zoo):
                return "Error: la funcion tiende a infinito en ese punto", None
            
            # simplificar el resultado
            resultado = sp.simplify(resultado)
            
            pasos = self.obtener_pasos_evaluacion_detallada(f_x, x_val, resultado)
            return float(resultado), pasos

        except sp.SympifyError:
            return "Error: funcion no valida", None
        except ZeroDivisionError:
            return "Error: division por cero en ese punto", None
        except Exception as e:
            return f"Error inesperado: {e}", None

    def obtener_pasos_evaluacion_detallada(self, f_x, x_val, resultado):
        """
        genera pasos detallados de la evaluacion mostrando cada calculo
        """
        x = sp.Symbol('x')
        pasos = []
        
        # paso 1: funcion original
        pasos.append(f"1. Funcion original: f(x) = {f_x}")
        
        # paso 2: sustitucion
        pasos.append(f"2. Sustituyendo x = {x_val}:")
        
        # paso 3: mostrar la sustitucion
        f_sustituida = str(f_x).replace('x', f'({x_val})')
        pasos.append(f"3. f({x_val}) = {f_sustituida}")
        
        # paso 4: calculos intermedios si es necesario
        try:
            # evaluar paso a paso para funciones mas complejas
            expr_intermedia = f_x.subs(x, x_val)
            
            # si hay potencias o multiplicaciones, mostrar esos calculos
            if '**' in str(f_x) or '*' in str(f_x):
                # expandir la expresion para mostrar calculos
                expanded = sp.expand(expr_intermedia)
                if expanded != expr_intermedia and expanded != resultado:
                    pasos.append(f"4. Calculando: {expanded}")
                    
        except:
            pass
        
        # resultado final
        paso_final = len(pasos) + 1
        pasos.append(f"{paso_final}. Resultado: f({x_val}) = {resultado}")
        pasos.append(f"{paso_final + 1}. Punto en la grafica: ({x_val}, {resultado})")
        
        return pasos

    def esta_en_dominio(self, f_x, x_val):
        """
        revisa si un valor pertenece al dominio de una funcion
        """
        x = sp.Symbol('x')

        try:
            # revisar denominadores
            denominador = sp.denom(f_x)
            if denominador != 1:
                valor_denominador = denominador.subs(x, x_val)
                if valor_denominador == 0:
                    return False
            
            # revisar que no genere numeros complejos
            resultado_prueba = f_x.subs(x, x_val)
            if resultado_prueba.is_complex or resultado_prueba.has(sp.I):
                return False
                
            return True
            
        except:
            return False

    def calcular_dominio(self, funcion_str):
        """
        calcula el dominio con explicacion paso a paso
        """
        # validar funcion primero
        es_valida, mensaje = self.validar_funcion(funcion_str)
        if not es_valida:
            return f"Error: {mensaje}", []

        try:
            x = sp.Symbol('x')
            f_x = sp.sympify(funcion_str)
            
            pasos = []
            pasos.append(f"1. Funcion: f(x) = {f_x}")
            pasos.append("2. Para encontrar el dominio, buscamos valores que hagan la funcion indefinida")

            restricciones = []

            # revisar denominadores
            denominador = sp.denom(f_x)
            if denominador != 1:
                pasos.append(f"3. El denominador es: {denominador}")
                pasos.append("4. El denominador no puede ser cero, resolvemos:")
                pasos.append(f"   {denominador} = 0")
                
                zeros = sp.solve(denominador, x)
                zeros_reales = [z for z in zeros if z.is_real]
                
                if zeros_reales:
                    pasos.append(f"5. Valores que hacen cero el denominador: {zeros_reales}")
                    restricciones.extend(zeros_reales)
                else:
                    pasos.append("5. No hay valores reales que hagan cero el denominador")
            else:
                pasos.append("3. La funcion es polinomica (no tiene denominador)")

            # resultado del dominio
            if not restricciones:
                dominio_str = "todos los numeros reales"
                pasos.append("6. Dominio: todos los numeros reales")
            else:
                dominio_str = f"todos los reales excepto x = {', '.join(map(str, restricciones))}"
                pasos.append(f"6. Dominio: {dominio_str}")

            return dominio_str, pasos

        except Exception as e:
            return f"Error al calcular dominio: {e}", []

    def calcular_intersecciones(self, funcion_str):
        # primero valida la funcion
        es_valida, mensaje = self.validar_funcion(funcion_str)
        if not es_valida:
            return f"Error: {mensaje}", [], f"Error: {mensaje}", []

        try:
            x = sp.Symbol('x')
            f_x = sp.sympify(funcion_str)

            # pasos para interseccion con eje y
            pasos_y = []
            pasos_y.append(f"1. Funcion: f(x) = {f_x}")
            pasos_y.append("2. Para interseccion con eje Y, evaluamos f(0):")

            if self.esta_en_dominio(f_x, 0):
                y_val = f_x.subs(x, 0)
                pasos_y.append(f"3. f(0) = {f_x.subs(x, 0)}")
                
                if not y_val.has(sp.I) and not y_val.has(sp.oo):
                    y_val = sp.simplify(y_val)
                    pasos_y.append(f"4. Interseccion con eje Y: (0, {y_val})")
                    interseccion_y = f"(0, {y_val})"
                else:
                    pasos_y.append("4. El resultado no es un numero real")
                    interseccion_y = "no existe"
            else:
                pasos_y.append("3. x = 0 no esta en el dominio")
                pasos_y.append("4. No hay interseccion con eje Y")
                interseccion_y = "no existe"

            # pasos para intersecciones con eje x
            pasos_x = []
            pasos_x.append(f"1. Funcion: f(x) = {f_x}")
            pasos_x.append("2. Para intersecciones con eje X, resolvemos f(x) = 0:")
            pasos_x.append(f"3. {f_x} = 0")

            soluciones = sp.solve(f_x, x)
            pasos_x.append(f"4. Soluciones encontradas: {soluciones}")

            x_int_reales = []
            for sol in soluciones:
                if sol.is_real and self.esta_en_dominio(f_x, sol):
                    x_int_reales.append(sol)

            if x_int_reales:
                puntos = [f"({sol}, 0)" for sol in x_int_reales]
                interseccion_x = f"Puntos: {', '.join(puntos)}"
                pasos_x.append(f"5. Intersecciones con eje X: {interseccion_x}")
            else:
                interseccion_x = "no existen intersecciones reales"
                pasos_x.append("5. No hay intersecciones reales con eje X")

            return interseccion_y, pasos_y, interseccion_x, pasos_x

        except Exception as e:
            error_msg = f"Error al calcular intersecciones: {e}"
            return error_msg, [], error_msg, []

    # recorrido de la funcion (placeholder)
    def calcular_recorrido(self, funcion_str):
        """
        calcula el recorrido de la funcion
        """
        return "no implementado aun", []