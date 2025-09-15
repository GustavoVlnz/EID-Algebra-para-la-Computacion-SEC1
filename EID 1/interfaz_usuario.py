from PyQt6 import QtWidgets, QtGui, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import math
import sympy as sp

from analisis_funciones import AnalizadorFunciones

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(6, 4), tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador de funciones")
        self.resize(1100, 680)
        self.backend = AnalizadorFunciones()
        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        root = QtWidgets.QHBoxLayout(central)

        # Izquierda: inputs y resultados
        left = QtWidgets.QVBoxLayout()
        root.addLayout(left, 3)

        form = QtWidgets.QFormLayout()
        left.addLayout(form)

        self.ed_func = QtWidgets.QLineEdit()
        self.ed_func.setPlaceholderText("Ej.: (x-1)/(x+2)  |  sqrt(x+1)  |  Abs(x)")
        self.ed_func.setClearButtonEnabled(True)
        form.addRow("Función f(x):", self.ed_func)

        self.ed_x = QtWidgets.QLineEdit()
        self.ed_x.setPlaceholderText("x opcional. Ej.: 2  |  -0.5  |  3/5")
        self.ed_x.setClearButtonEnabled(True)
        # Validador: número o fracción a/b. Soporta .5, 1e-3 y espacios.
        rx = QtCore.QRegularExpression(r"^\s*[-+]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+\-]?\d+)?(?:\s*/\s*[-+]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+\-]?\d+)?)?\s*$")
        self.ed_x.setValidator(QtGui.QRegularExpressionValidator(rx))
        form.addRow("Valor de x:", self.ed_x)

        btn_row = QtWidgets.QHBoxLayout()
        left.addLayout(btn_row)
        self.btn_run = QtWidgets.QPushButton("Analizar y graficar")
        self.btn_clear = QtWidgets.QPushButton("Limpiar")
        btn_row.addWidget(self.btn_run)
        btn_row.addWidget(self.btn_clear)

        self.out = QtWidgets.QTextEdit()
        self.out.setReadOnly(True)
        self.out.setPlaceholderText("Aquí verás dominio, recorrido, intersecciones y el paso a paso.")
        self.out.setFont(QtGui.QFont("Consolas", 10))
        left.addWidget(self.out, 1)

        # Derecha: gráfico embebido
        right = QtWidgets.QVBoxLayout()
        root.addLayout(right, 4)
        self.canvas = MplCanvas(self)
        right.addWidget(self.canvas)

        # Eventos
        self.btn_run.clicked.connect(self._run)
        self.btn_clear.clicked.connect(self._clear)

    # ---------- Utilidades ----------
    def _linspace(self, a: float, b: float, n: int):
        if n < 2:
            return [a]
        step = (b - a) / (n - 1)
        return [a + i * step for i in range(n)]

    def _cluster_around(self, c: float, eps: float = 1e-3):
        # puntos densos alrededor de c para dibujar cerca de asintotas/fronteras
        return [c - 10*eps, c - 3*eps, c - eps, c - eps/3, c - eps/10,
                c + eps/10, c + eps/3, c + eps, c + 3*eps, c + 10*eps]

    def _plot_function(self, f_str: str, punto=None, inters=None,
                       x_min=-10, x_max=10, base_pts=800, y_clip=50.0):
        ax = self.canvas.ax
        ax.clear()

        # Preparar expresión
        x = sp.Symbol('x', real=True)
        try:
            f = self.backend._sympify(f_str)
        except Exception:
            raise ValueError("Función inválida.")

        # Muestreo base + clusters en puntos críticos
        xs = self._linspace(x_min, x_max, base_pts)
        # Para asintotas se puede mejorar, de momento simple
        xs = sorted(set(xs))

        # Evaluación segura punto a punto
        ys = []
        for xv in xs:
            try:
                yv = f.subs(x, xv)
                if yv.is_real is False:
                    ys.append(None); continue
                y = float(yv)
                if not math.isfinite(y) or abs(y) > y_clip:
                    ys.append(None)
                else:
                    ys.append(y)
            except Exception:
                ys.append(None)

        # Trazo por segmentos (corta en None)
        segx, segy = [], []
        def flush(label_needed=False):
            nonlocal segx, segy
            if segx:
                ax.plot(segx, segy, linewidth=2.0,
                        label=f"f(x) = {f_str}" if label_needed else "")
                segx, segy = [], []

        first = True
        for xv, yv in zip(xs, ys):
            if yv is None:
                flush(label_needed=first); first = False
            else:
                segx.append(xv); segy.append(yv)
        flush(label_needed=first)

        # Pintar asintotas verticales donde el dominio excluye el punto crítico
        for c in critical:
            ax.axvline(c, linewidth=0.8, linestyle=':', alpha=0.7)

        # Intersecciones
        if inters:
            if inters.get("x"):
                for i, xi in enumerate(inters["x"]):
                    ax.plot([xi], [0.0], marker='o', markersize=6,
                            label="Intersección X" if i == 0 else "")
            if inters.get("y"):
                ax.plot([inters["y"][0]], [inters["y"][1]], marker='o', markersize=6, label="Intersección Y")

        # Punto evaluado en color distinto
        if punto:
            ax.plot([punto[0]], [punto[1]], marker='o', markersize=8, label=f"Punto ({punto[0]}, {punto[1]})")

        ax.axhline(0, linewidth=0.8, linestyle='--')
        ax.axvline(0, linewidth=0.8, linestyle='--')
        ax.grid(True, which='both', linewidth=0.3)
        ax.set_title("Gráfico")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()
        self.canvas.draw()

    # ---------- Acciones ----------
    def _run(self):
        fstr = self.ed_func.text().strip()
        vstr = self.ed_x.text().strip()

        if not fstr:
            QtWidgets.QMessageBox.warning(self, "Entrada", "Ingresa la función.")
            return

        # Analítica
        dominio, pasos_dom = self.backend.calcular_dominio(fstr)
        recorrido, pasos_rec = self.backend.calcular_recorrido(fstr)
        inters_y, pasos_y, inters_x, pasos_x = self.backend.calcular_intersecciones(fstr)

        inters_dict = {"y": None, "x": []}
        if not isinstance(inters_y, str) and inters_y != "no existe":
            try:
                y_val = float(str(inters_y).strip("()").split(",")[1])
                inters_dict["y"] = (0.0, y_val)
            except Exception:
                pass
        if "Puntos:" in inters_x:
            try:
                puntos = inters_x.replace("Puntos:", "").split(",")
                inters_dict["x"] = [float(p.strip("() ").split(",")[0]) for p in puntos]
            except Exception:
                pass

        # Paso a paso en la salida
        lines = []
        lines.append("=== Dominio ===")
        lines.extend(pasos_dom)
        lines.append("") 
        lines.append("=== Recorrido ===")
        lines.extend(pasos_rec)
        lines.append("")
        lines.append("=== Intersección con eje Y ===")
        lines.extend(pasos_y)
        lines.append("")
        lines.append("=== Intersecciones con eje X ===")
        lines.extend(pasos_x)

        punto = None
        if vstr:
            res = self.backend.evaluar_funcion(fstr, vstr)
            lines.append("\n--- Evaluación ---")
            lines.extend(res.get("steps", []))
            if res.get("ok"):
                lines.append(f"Par ordenado: ({res['x_num']}, {res['value']})")
                punto = (res['x_num'], res['value'])
            else:
                lines.append(res.get("error", "Error en evaluación."))

        self.out.clear()
        self.out.setPlainText("\n".join(lines))

        # Gráfico
        try:
            self._plot_function(fstr, punto=punto, inters=inters_dict)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Gráfico", f"No se pudo graficar: {e}")

    def _clear(self):
        self.ed_func.clear()
        self.ed_x.clear()
        self.out.clear()
        self.canvas.ax.clear()
        self.canvas.draw()
