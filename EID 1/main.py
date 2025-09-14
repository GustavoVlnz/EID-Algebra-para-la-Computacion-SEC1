import sys
import tkinter as tk
from analisis_funciones import AnalizadorFunciones
from interfaz_usuario import AnalizadorFunciones
from interfaz_usuario import MainWindow
from PyQt6 import QtWidgets

def main():
    app = AnalizadorFunciones()
    # Inicia el bucle de la aplicacion
    app.mainloop()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
