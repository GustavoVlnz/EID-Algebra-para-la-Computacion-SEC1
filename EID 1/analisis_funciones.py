import sympy as sp
from sympy import S
from sympy.calculus.util import continuous_domain, function_range
from sympy.solvers.solveset import solveset, solveset_real
import re, unicodedata

class AnalizadorFunciones:
    FUNCIONES_PERMITIDAS = {
        # funciones
        'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
        'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
        'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
        'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
        'Abs': sp.Abs, 'Piecewise': sp.Piecewise,
        'floor': sp.floor, 'ceiling': sp.ceiling,
        # constantes
        'E': sp.E, 'pi': sp.pi,
    }

    def __init__(self):
        self._RE_NUM = re.compile(
            r'^[+\-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+\-]?\d+)?'
            r'(?:/[+\-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+\-]?\d+)?)?$'
        )

    def _sympify(self, s: str):
        """Parse controlado: solo símbolo x y nombres permitidos."""
        if not isinstance(s, str) or len(s) > 500:
            raise ValueError("Expresión inválida o demasiado larga.")
        x = sp.Symbol('x', real=True)
        expr = sp.sympify(s, locals={**self.FUNCIONES_PERMITIDAS, 'x': x})
        # bloquear símbolos extraños
        if any(sym.name != 'x' for sym in expr.free_symbols):
            raise ValueError("Solo se admite la variable x.")
        return expr

    def _pretty(self, expr) -> str:
        from sympy.printing.pretty import pretty
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

    def _sanitize_number(self, s: str) -> str:
        # Normaliza Unicode, cambia coma por punto, quita espacios y guiones Unicode
        s = unicodedata.normalize('NFKC', s)
        s = s.replace('\u2212','-').replace('\u2012','-').replace('\u2013','-').replace('\u2014','-').replace('\u2015','-')
        s = re.sub(r'\s+', '', s)
        s = s.replace(',', '.')
        return s

    def _to_exact(self, val_str: str):
        if not val_str or val_str.strip() == "":
            raise ValueError("Valor vacío.")
        s = self._sanitize_number(val_str)
        if not self._RE_NUM.fullmatch(s):
            raise ValueError("Valor inválido para evaluar.")
        # fracción
        if '/' in s:
            a, b = s.split('/', 1)
            a = sp.nsimplify(a)
            b = sp.nsimplify(b)
            if b == 0:
                raise ValueError("División por cero en el valor.")
            return a / b
        # número simple
        return sp.nsimplify(s)

    def _denominador(self, f):
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

    def evaluar_funcion(self, funcion_str: str, x_val_str: str):
        x = sp.Symbol('x', real=True)
        pasos = []
        try:
            f = self._sympify(funcion_str)
        except Exception:
            return {"ok": False, "error": "Función inválida.", "steps": []}

        except sp.SympifyError:
            return "Error: funcion no valida", None
        except ZeroDivisionError:
            return "Error: division por cero en ese punto", None
        except Exception as e:
            return f"Error inesperado: {e}", None

        pasos.append(f"Función: f(x) = {self._pretty(f)}")
        pasos.append(f"Sustitución: x = {self._pretty(xv)}")

        # Validación de dominio puntual
        try:
            den = self._denominador(f)
            if sp.simplify(den.subs(x, xv)) == 0:
                pasos.append("Denominador = 0 ⇒ punto fuera del dominio.")
                return {"ok": False, "error": "División por cero en ese punto.", "steps": pasos}
        except Exception:
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

            # Chequeos
            if exacto.has(sp.I) or (hasattr(exacto, "is_real") and exacto.is_real is False):
                return {"ok": False, "error": "Resultado complejo.", "steps": pasos}
            if exacto.has(sp.zoo) or exacto.has(sp.oo) or exacto.has(-sp.oo):
                return {"ok": False, "error": "Resultado no finito.", "steps": pasos}

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

        # Intersección con eje Y si 0 ∈ dominio
        y_pair = None
        try:
            dom0 = continuous_domain(f, x, S.Reals)
            if 0 in dom0:
                y0 = f.subs(x, 0)
                if y0.is_real is not False:
                    y_pair = (0.0, float(sp.N(y0)))
        except Exception:
            pass

        # Raíces reales
        x_list = []
        try:
            sol = solveset(sp.Eq(f, 0), x, domain=S.Reals)
            for s in sol:
                try:
                    x_list.append(float(sp.N(s)))
                except Exception:
                    continue
        except Exception:
            try:
                sol2 = solveset_real(sp.Eq(f, 0), x)
                for s in sol2:
                    x_list.append(float(sp.N(s)))
            except Exception:
                pass

        return {"y": y_pair, "x": x_list}

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

    def calcular_recorrido(self, funcion_str):
        """
        Calcula el recorrido de la función con pasos explicativos.
        """
        # validar primero
        es_valida, mensaje = self.validar_funcion(funcion_str)
        if not es_valida:
            return f"Error: {mensaje}", []

        try:
            if isinstance(f, sp.Piecewise):
                for _, cond in f.as_expr_set_pairs():
                    if hasattr(cond, 'boundary'):
                        b = cond.boundary
                        for el in getattr(b, 'args', (b,)):
                            try:
                                for s in getattr(el, 'args', (el,)):
                                    if getattr(s, "is_number", False):
                                        critical.add(float(sp.N(s)))
                            except Exception:
                                continue
        except Exception:
            pass

            pasos = []
            pasos.append(f"1. Función: f(x) = {f_x}")
            pasos.append("2. Usamos análisis simbólico para determinar el rango.")

            # rango con sympy
            recorrido = function_range(f_x, x, sp.S.Reals)

            pasos.append(f"3. El recorrido calculado es: {recorrido}")

            return str(recorrido), pasos

        except Exception as e:
            return f"Error al calcular recorrido: {e}", []
