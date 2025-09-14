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
            return pretty(expr)
        except Exception:
            return str(expr)

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
            return sp.denom(sp.together(f))
        except Exception:
            return S.One

    def evaluar_funcion(self, funcion_str: str, x_val_str: str):
        x = sp.Symbol('x', real=True)
        pasos = []
        try:
            f = self._sympify(funcion_str)
        except Exception:
            return {"ok": False, "error": "Función inválida.", "steps": []}

        try:
            xv = self._to_exact(x_val_str)
        except ValueError as e:
            return {"ok": False, "error": str(e), "steps": []}

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

        # Paso a paso
        try:
            expr_sub = f.subs(x, xv)
            pasos.append(f"1) Tras sustitución:\n{self._pretty(expr_sub)}")

            expr_together = sp.together(expr_sub)
            if expr_together != expr_sub:
                pasos.append(f"2) Unificar fracciones:\n{self._pretty(expr_together)}")

            expr_cancel = sp.cancel(expr_together)
            if expr_cancel != expr_together:
                pasos.append(f"3) Cancelar factores:\n{self._pretty(expr_cancel)}")

            expr_simpl = sp.simplify(expr_cancel)
            if expr_simpl != expr_cancel:
                pasos.append(f"4) Simplificar:\n{self._pretty(expr_simpl)}")

            exacto = sp.simplify(expr_simpl)

            # Chequeos
            if exacto.has(sp.I) or (hasattr(exacto, "is_real") and exacto.is_real is False):
                return {"ok": False, "error": "Resultado complejo.", "steps": pasos}
            if exacto.has(sp.zoo) or exacto.has(sp.oo) or exacto.has(-sp.oo):
                return {"ok": False, "error": "Resultado no finito.", "steps": pasos}

            pasos.append(f"5) Valor exacto:\n{self._pretty(exacto)}")
            approx = sp.N(exacto)
            pasos.append(f"6) Valor decimal: {approx}")

            return {
                "ok": True,
                "value": float(approx),
                "value_exact": str(exacto),
                "steps": pasos,
                "x_num": float(sp.N(xv))
            }
        except ZeroDivisionError:
            return {"ok": False, "error": "División por cero durante la evaluación.", "steps": pasos}
        except Exception as e:
            return {"ok": False, "error": f"Error inesperado: {e}", "steps": pasos}

    def calcular_dominio(self, funcion_str: str) -> str:
        x = sp.Symbol('x', real=True)
        try:
            f = self._sympify(funcion_str)
            dom = continuous_domain(f, x, S.Reals)
            return str(dom)
        except Exception:
            return "No determinado"

    def calcular_recorrido(self, funcion_str: str) -> str:
        x = sp.Symbol('x', real=True)
        try:
            f = self._sympify(funcion_str)
            rng = function_range(f, x, S.Reals)
            return str(rng)
        except Exception:
            return "No determinado"

    def calcular_intersecciones(self, funcion_str: str):
        x = sp.Symbol('x', real=True)
        try:
            f = self._sympify(funcion_str)
        except Exception:
            return {"y": None, "x": []}

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

    def puntos_criticos_para_grafico(self, funcion_str: str):
        """Candidatos a discontinuidad: ceros del denominador y fronteras de Piecewise."""
        x = sp.Symbol('x', real=True)
        critical = set()
        try:
            f = self._sympify(funcion_str)
        except Exception:
            return critical

        # Denominador = 0
        try:
            den = self._denominador(f)
            if den != 1:
                Sset = solveset(den, x, domain=S.Reals)
                for s in Sset:
                    try:
                        critical.add(float(sp.N(s)))
                    except Exception:
                        continue
        except Exception:
            pass

        # Fronteras de Piecewise
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

        return critical
