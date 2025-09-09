import sys
import tkinter as tk
from analisis_funciones import AnalizadorFunciones
from interfaz_usuario import AnalizadorFuncionesGUI

def main():
    backend = AnalizadorFunciones()
    
    # Crea la ventana principal de Tkinter
    app = AnalizadorFuncionesGUI(backend)
    
    # Inicia el bucle de la aplicacion
    app.mainloop()

if __name__ == "__main__":
    main()
